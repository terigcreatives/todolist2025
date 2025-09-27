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
function handleDeleteClick(link) {
    if (!confirm('Are you sure you want to delete this task?')) return;
    const taskId = link.getAttribute('data-task-id');
    const form = document.getElementById('deleteTaskForm');
    form.action = `/task/delete/${taskId}/`;
    form.submit();
}

/////////
    // Toggle show/hide completed tasks
    document.getElementById("toggleCompleted").addEventListener("click", function () {
        let completedList = document.getElementById("completedTasks");
        if (completedList.style.display === "none") {
            completedList.style.display = "block";
            this.textContent = "▶ Hide Completed Tasks";
        } else {
            completedList.style.display = "none";
            this.textContent = "▼ Show Completed Tasks";
        }
    });

// Modal functions
// function openAddTaskModal() {
//     document.getElementById('modalTitle').textContent = 'Add New Task';
//     document.getElementById('taskForm').reset();
//     // Set today's date as default
//     const today = new Date().toISOString().split('T')[0];
//     document.getElementById('taskDate').value = today;
//     document.getElementById('taskModal').classList.remove('hidden');
// }
// function closeAddTaskModal() {
//     document.getElementById('taskModal').classList.add('hidden');
// }

let subtaskCounter = 0;

// For new subtasks
function addSubtaskField(title = '', completed = false) {
    subtaskCounter++;
    const subtasksList = document.getElementById('subtasksList');
    const div = document.createElement('div');
    div.className = 'flex items-center mb-2 subtask-row';
    div.innerHTML = `
        <input type="text" name="subtask_title_new_${subtaskCounter}" value="${title}" placeholder="Subtask" class="w-2/3 border rounded px-2 py-1 mr-2">
        <label class="mr-2">
            <input type="checkbox" name="subtask_completed_new_${subtaskCounter}" ${completed ? 'checked' : ''}> Done
        </label>
        <button type="button" onclick="this.parentElement.remove()" class="text-red-500 ml-2"><i class="fi fi-rr-trash"></i></button>
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

// When opening the modal for editing
// function openEditTaskModal(id, title, description, priority, dueDate, dueTime, subtasks) {
//     document.getElementById('modalTitle').textContent = 'Edit Task';
//     document.getElementById('taskForm').action = `/editTask/${id}/`;
//     document.getElementById('editTaskId').value = id;
//     document.getElementById('taskForm').reset();
//     document.querySelector('input[name="title"]').value = title;
//     document.querySelector('textarea[name="description"]').value = description;
//     document.querySelector('select[name="priority"]').value = priority;
//     document.getElementById('taskDate').value = dueDate;
//     document.getElementById('taskTime').value = dueTime;

//     // Clear and add subtasks
//     document.getElementById('subtasksList').innerHTML = '';
//     subtaskCounter = 0;
//     if (subtasks && subtasks.length) {
//         subtasks.forEach(function(subtask) {
//             addExistingSubtaskField(subtask.id, subtask.title, subtask.completed);
//         });
//     }
//     document.getElementById('taskModal').classList.remove('hidden');
// }

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

    // Subtasks
    document.getElementById('subtasksList').innerHTML = '';
    subtaskCounter = 0;
    if (subtasks && subtasks.length) {
        subtasks.forEach(function(subtaskTitle) {
            subtaskCounter++;
            const input = document.createElement('input');
            input.type = 'text';
            input.name = `subtask_${subtaskCounter}`;
            input.className = 'w-full border rounded px-3 py-2 mb-2';
            input.placeholder = `Subtask ${subtaskCounter}`;
            input.value = subtaskTitle;
            document.getElementById('subtasksList').appendChild(input);
        });
    }

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
