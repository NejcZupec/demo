from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm, TaskEditForm

# Create your views here.

def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    form = TaskForm()
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    
    return render(request, 'todo/task_list.html', {
        'tasks': tasks,
        'form': form
    })

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskEditForm(instance=task)
    
    return render(request, 'todo/edit_task.html', {
        'form': form,
        'task': task
    })

def update_status(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            return JsonResponse({
                'status': 'success',
                'task_status': task.status,
                'task_status_display': task.get_status_display()
            })
    return JsonResponse({'status': 'error'}, status=400)
