from django.shortcuts import render, redirect, get_object_or_404
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
