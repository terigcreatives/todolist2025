// JS from main.html
function openAddTaskModal() {
    document.getElementById('modalTitle').textContent = 'Add New Task';
    document.getElementById('taskForm').reset();
    // Set today's date as default
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('taskDate').value = today;
    document.getElementById('taskModal').classList.remove('hidden');
}
function closeAddTaskModal() {
    document.getElementById('taskModal').classList.add('hidden');
}

// Delete icon feature using <a>
function handleDeleteClick(btn) {
    if (!confirm('Are you sure you want to delete this task?')) return;
    const taskId = link.getAttribute('data-task-id');
    const form = document.getElementById('deleteTaskForm');
    form.action = `/task/delete/${taskId}/`;
    form.submit();
}

////////

let subtaskCounter = 0;

// For new subtasks
function addSubtaskField() {
    subtaskCounter++;
    const subtasksList = document.getElementById('subtasksList');
    const div = document.createElement('div');
    div.className = 'flex items-center space-x-2';
    div.innerHTML = `
        <input type="text" name="subtask_title[]" 
                placeholder="Subtask title" 
                class="w-2/3 border rounded px-2 py-1 mr-2">

        <!-- hidden + checkbox pair -->
        <label class="mr-2"> 
            <input type="hidden" name="subtask_title[]" value="0">
            <input type="checkbox" name="subtask_completed[]" 
                value="1" class="accent-green-500"> Done
        </label>

        <!-- Delete icon -->
        <button type="button" onclick="handleDeleteClick(btn)>
        <i class="fi fi-rr-trash"></i></button>

    `;
    subtasksList.appendChild(div);
}


// For existing subtasks (when editing)
function addExistingSubtaskField(id, title, completed) {
    const subtasksList = document.getElementById('subtasksList');
    const idx = id;
    const div = document.createElement('div');
    div.className = 'flex items-center mb-2 subtask-row';
    div.innerHTML = `
        <input type="hidden" name="subtask_id_${idx}" value="${id}">
        <input type="text" name="subtask_title_${idx}" value="${title}" class="w-2/3 border rounded px-2 py-1 mr-2">
        <label class="mr-2">
            <input type="checkbox" name="subtask_completed_${idx}" ${completed ? 'checked' : ''}> Done
        </label>
        <label class="mr-2">
            <input type="checkbox" name="subtask_delete_${idx}"> Delete
        </label>
        <button type="button" onclick="this.parentElement.remove()" class="text-red-500 ml-2">🗑️</button>
    `;
    subtasksList.appendChild(div);
}


// Optional: Reset subtasks when opening modal
function openAddTaskModal() {
    document.getElementById('modalTitle').textContent = 'Add New Task';
    document.getElementById('taskForm').reset();
    document.getElementById('subtasksList').innerHTML = '';
    subtaskCounter = 0;
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('taskDate').value = today;
    document.getElementById('taskModal').classList.remove('hidden');
}

function openEditTaskModal(id, title, description, priority, dueDate, dueTime, subtasks) {
    document.getElementById('modalTitle').textContent = 'Edit Task';
    document.getElementById('taskForm').action = `/editTask/${id}`; // Update form action
    document.getElementById('editTaskId').value = id;
    document.getElementById('taskForm').reset();

    document.querySelector('input[name="title"]').value = title;
    document.querySelector('textarea[name="description"]').value = description;
    document.querySelector('select[name="priority"]').value = priority;
    document.getElementById('taskDate').value = dueDate;
    document.getElementById('taskTime').value = dueTime;

    // Clear and render existing subtasks (id, title, completed)
    const list = document.getElementById('subtasksList');
    list.innerHTML = '';
    subtaskCounter = 0;

    // Expect subtasks to be an array of objects: [{id, title, completed}]
    if (Array.isArray(subtasks)) {
        subtasks.forEach(s => {
            if (!s) return;
            addExistingSubtaskField(s.id, s.title, !!s.completed);
        });
    }

    // User can add more while editing using the existing "+ Add Subtask" button
    document.getElementById('taskModal').classList.remove('hidden');
}

function handleEditClick(btn) {
    const id = btn.getAttribute('data-task-id');
    const title = btn.getAttribute('data-title');
    const description = btn.getAttribute('data-description');
    const priority = btn.getAttribute('data-priority');
    const dueDate = btn.getAttribute('data-due-date');
    const dueTime = btn.getAttribute('data-due-time');

// JSON Approach(with JSON.parse)
    const subtasksRaw = btn.getAttribute('data-subtasks');
    let subtasks = [];
    try {
        subtasks = subtasksRaw ? JSON.parse(subtasksRaw) : [];
    } catch (e) {
        subtasks = [];
    }

    openEditTaskModal(id, title, description, priority, dueDate, dueTime, subtasks);
    // handleEditClick(id, title, description, priority, dueDate, dueTime, subtasks);
}
