document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const tasks = document.querySelectorAll('.task-item');
    const dropZones = document.querySelectorAll('.column-drop-zone');
    let draggedTask = null;
    let placeholder = null;
    let isDragging = false;

    // Add drag and drop event listeners to tasks
    tasks.forEach(task => {
        task.addEventListener('dragstart', handleDragStart);
        task.addEventListener('dragend', handleDragEnd);
        // Cancel drag if mouse is released without proper drag
        task.addEventListener('mouseup', function(e) {
            if (!isDragging && this.style.display === 'none') {
                this.style.display = 'block';
            }
        });
    });

    // Add drop zone event listeners
    dropZones.forEach(zone => {
        zone.addEventListener('dragenter', handleDragEnter);
        zone.addEventListener('dragover', handleDragOver);
        zone.addEventListener('dragleave', handleDragLeave);
        zone.addEventListener('drop', handleDrop);
    });

    function createPlaceholder() {
        const div = document.createElement('div');
        div.className = 'task-placeholder';
        return div;
    }

    function handleDragStart(e) {
        // Prevent drag start if clicking on the Edit button
        if (e.target.closest('.btn')) {
            e.preventDefault();
            return;
        }

        isDragging = true;
        draggedTask = this;
        this.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', this.dataset.taskId);
        
        // Create placeholder with same dimensions as dragged task
        placeholder = createPlaceholder();
        placeholder.style.height = `${this.offsetHeight}px`;
        
        // Hide original task after a short delay
        requestAnimationFrame(() => {
            if (isDragging) {
                this.style.display = 'none';
            }
        });
    }

    function handleDragEnd(e) {
        isDragging = false;
        this.classList.remove('dragging');
        this.style.display = 'block';
        
        if (placeholder && placeholder.parentNode) {
            placeholder.parentNode.removeChild(placeholder);
        }
        
        dropZones.forEach(zone => zone.classList.remove('drag-over'));
        draggedTask = null;
        placeholder = null;
    }

    function handleDragEnter(e) {
        e.preventDefault();
        if (isDragging) {
            this.classList.add('drag-over');
        }
    }

    function handleDragOver(e) {
        e.preventDefault();
        if (!isDragging) return;
        
        e.dataTransfer.dropEffect = 'move';
        
        const dropZone = this;
        const afterElement = getDragAfterElement(dropZone, e.clientY);
        
        if (placeholder) {
            if (afterElement) {
                afterElement.parentNode.insertBefore(placeholder, afterElement);
            } else {
                dropZone.appendChild(placeholder);
            }
        }
    }

    function getDragAfterElement(container, y) {
        const draggableElements = [...container.querySelectorAll('.task-item:not(.dragging), .task-placeholder')];
        
        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            
            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child };
            } else {
                return closest;
            }
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }

    function handleDragLeave(e) {
        if (e.target === this) {
            this.classList.remove('drag-over');
        }
    }

    function handleDrop(e) {
        e.preventDefault();
        this.classList.remove('drag-over');
        
        if (!draggedTask || !isDragging) return;

        const newStatus = this.parentElement.dataset.status;
        const taskId = draggedTask.dataset.taskId;
        const formData = new FormData();
        formData.append('status', newStatus);

        // Update task status via API
        fetch(`/task/${taskId}/update-status/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Insert the task at the placeholder position
                if (placeholder && placeholder.parentNode) {
                    placeholder.parentNode.insertBefore(draggedTask, placeholder);
                    placeholder.parentNode.removeChild(placeholder);
                } else {
                    this.appendChild(draggedTask);
                }
                
                // Update task styling if completed
                const taskTitle = draggedTask.querySelector('.task-title');
                if (newStatus === 'completed') {
                    taskTitle.classList.add('text-decoration-line-through', 'text-muted');
                } else {
                    taskTitle.classList.remove('text-decoration-line-through', 'text-muted');
                }
                
                draggedTask.style.display = 'block';
            } else {
                console.error('Error updating task:', data.message);
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            window.location.reload();
        });
    }
}); 