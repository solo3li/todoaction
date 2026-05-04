from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo

def todo_list(request):
    todos = Todo.objects.all().order_by('-created_at')
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Todo.objects.create(title=title)
        return redirect('todo_list')
    return render(request, 'todos/todo_list.html', {'todos': todos})

def toggle_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')

def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect('todo_list')
