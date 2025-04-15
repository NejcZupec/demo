from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Task
from .forms import TaskForm, TaskEditForm

# Create your views here.


def task_list(request):
    """Display list of tasks and handle new task creation."""
    tasks = Task.objects.all().order_by('-created_at')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    context = {
        'tasks': tasks,
        'form': form
    }
    return render(request, 'todo/task_list.html', context)


def edit_task(request, task_id):
    """Handle editing of an existing task."""
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskEditForm(instance=task)

    context = {
        'form': form,
        'task': task
    }
    return render(request, 'todo/edit_task.html', context)


@require_http_methods(['POST'])
def update_status(request, task_id):
    """Update task status via AJAX request."""
    task = get_object_or_404(Task, id=task_id)
    new_status = request.POST.get('status')

    # Validate the new status
    if new_status not in dict(Task.STATUS_CHOICES):
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid status'
        }, status=400)

    # Update and save the task
    task.status = new_status
    task.save()

    # Return success response with updated task info
    return JsonResponse({
        'status': 'success',
        'task_status': task.status,
        'task_status_display': task.get_status_display(),
        'task_id': task.id
    })
