from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.template import loader
from .models import Task
from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.

# def home(request):
#     return HttpResponse("Hello! Your Django server is connected and running! 🎉")

@login_required
# View main page - All Tasks List
def tasklist(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == 'toggle_task':
            task_id = request.POST.get('task_id')
            task = Task.objects.get(id=task_id)
            task.completed = not task.completed
            task.save()
        return redirect(request.path)

    sort = request.GET.get('sort', 'created')
    now = timezone.now()
    today = now.date()
    tomorrow = today + timedelta(days=1)
    week_end = today + timedelta(days=7)

    # Determine which page is being requested
    page = request.resolver_match.url_name

    # To hide the active(incomplete) tasks on the completed page
    if page == 'completed':
        alltasks = Task.objects.filter(user=request.user).none() # No active tasks
        completedtasks = Task.objects.filter(user=request.user, completed=True, parent_task__isnull=True).prefetch_related('subtasks')
    else:
    # Base queryset: only top-level tasks; prefetch children
        alltasks = Task.objects.filter(user=request.user, completed=False, parent_task__isnull=True).prefetch_related('subtasks')
        completedtasks = Task.objects.filter(user=request.user, completed=True, parent_task__isnull=True).prefetch_related('subtasks')

    if page == 'today':
        alltasks = alltasks.filter(due_date__date=today)
        completedtasks = completedtasks.filter(due_date__date=today)
    elif page == 'tomorrow':
        alltasks = alltasks.filter(due_date__date=tomorrow)
        completedtasks = completedtasks.filter(due_date__date=tomorrow)
    elif page == 'this_week':
        alltasks = alltasks.filter(due_date__date__gte=today, due_date__date__lte=week_end)
        completedtasks = completedtasks.filter(due_date__date__gte=today, due_date__date__lte=week_end)
    elif page == 'planned':
        alltasks = alltasks.filter(due_date__date__gt=week_end)
        completedtasks = completedtasks.filter(due_date__date__gt=week_end)
    # else: show all tasks (for 'task_list')

    # Sorting
    if sort == 'priority':
        alltasks = alltasks.order_by('-priority', '-id')
        completedtasks = completedtasks.order_by('-priority', '-id')
    elif sort == 'due_date':
        alltasks = alltasks.order_by('due_date', '-id')
        completedtasks = completedtasks.order_by('due_date', '-id')
    elif sort == 'title':
        alltasks = alltasks.order_by('title', '-id')
        completedtasks = completedtasks.order_by('title', '-id')
    else:  # default: created
        alltasks = alltasks.order_by('-id')
        completedtasks = completedtasks.order_by('-id')

    return render(request, 'task_list.html', {
        'alltasks': alltasks,
        'completedtasks': completedtasks,
        'page': page,
    })


# View Add Task Form
@login_required
def add_task(request):
    if request.method == "POST":
        # Parse due date & time
        due_date_str = request.POST.get("due_date")  # e.g. '2025-09-18'
        due_time_str = request.POST.get("due_time")  # e.g. '14:30'
        due_datetime = None
        if due_date_str and due_time_str:
            due_datetime = datetime.strptime(f"{due_date_str} {due_time_str}", "%Y-%m-%d %H:%M")
        elif due_date_str:
            due_datetime = datetime.strptime(due_date_str, "%Y-%m-%d")

        # Create the main task
        task = Task.objects.create(
            user = request.user, # attach logged-in user
            title = request.POST.get('title'),
            description = request.POST.get('description'),
            priority = request.POST.get('priority'),
            due_date = due_datetime,
        )
        # Handle multiple subtasks; getlist() → all of them (even if you added 10 subtasks in the modal).
        # loop subtasks_title[] + subtasks_completed[]
        subtask_title = request.POST.getlist("subtask_title[]")
        subtask_completed = request.POST.getlist("subtask_completed[]")

        for i, title in enumerate(subtask_title):
            if title.strip():
                completed = (subtask_completed[i] == "1")if i < len(subtask_completed) else False
                Task.objects.create(
                    user=request.user,
                    title=title.strip(),
                    parent_task=task,
                    completed=completed
                )

        #Redirect to where user came from
        # next_url = request.POST.get('next')
        # if next_url and 'completed' not in next_url:
        #     return redirect(next_url)
        return redirect("task_list")
    
    return redirect("task_list")

# View Toggle for subtasks
def toggle_subtask(request, subtask_id):
    subtask = get_object_or_404(Task, id=subtask_id, user=request.user)
    if request.method == "POST":
        subtask.completed = not subtask.completed
        subtask.save()
    return redirect('task_list')

# View Edit Task
def edit_task(request, id):
    task = get_object_or_404(Task, id=id)
    subtasks_qs = task.subtasks.all()
    if request.method == "POST":
        # Update main task fields
        due_date_str = request.POST.get("due_date")
        due_time_str = request.POST.get("due_time")
        due_datetime = None
        if due_date_str and due_time_str:
            due_datetime = datetime.strptime(f"{due_date_str} {due_time_str}", "%Y-%m-%d %H:%M")
        elif due_date_str:
            due_datetime = datetime.strptime(due_date_str, "%Y-%m-%d")

        task.title = request.POST.get("title")
        task.description = request.POST.get('description')
        task.priority = request.POST.get('priority')
        task.due_date = due_datetime
        task.save()

        # --- Handle SubTasks CRUD ---
        # 1. Update or delete existing subtasks
        for key in request.POST:
            if key.startswith('subtask_id_'):
                idx = key.split('_')[-1]
                subtask_id = request.POST.get(f'subtask_id_{idx}')
                title = request.POST.get(f'subtask_title_{idx}', '').strip()
                completed = request.POST.get(f'subtask_completed_{idx}') == 'on'
                to_delete = request.POST.get(f'subtask_delete_{idx}') == 'on'
                if subtask_id:
                    try:
                        subtask = task.subtasks.get(id=subtask_id)
                        if to_delete:
                            subtask.delete()
                        else:
                            subtask.title = title
                            subtask.completed = completed
                            subtask.save()
                    except Task.DoesNotExist:
                        pass

        # 2. Add new subtasks (those with no ID)
        for key in request.POST:
            if key.startswith('subtask_title_new_'):
                idx = key.split('_')[-1]
                title = request.POST.get(f'subtask_title_new_{idx}', '').strip()
                completed = request.POST.get(f'subtask_completed_new_{idx}') == 'on'
                if title:
                    task.subtasks.create(user=request.user, title=title, completed=completed)

        # Redirect to the page the user was on
        # next_url = request.POST.get('next')
        # if next_url and 'completed' not in next_url:
        #     return redirect(next_url)
        return redirect("task_list")
        # For GET, you can render a page or just return nothing if using modal


def taskcompleted(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'toggle_task':
            task_id = request.POST.get('task_id')
            task = Task.objects.get(id=task_id)
            task.completed = not task.completed
            task.save()

        return redirect(request.path) # refresh completed.html
    
    completedtasks = Task.objects.filter(completed=True) # get completed tasks
    return render(request, 'completed.html', {'completedtasks': completedtasks})

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk) # pk means primary key field or id
    if request.method == "POST": # don't delete on GET -- destructive actions must use POST
        task.delete()
    return redirect('task_list')



    