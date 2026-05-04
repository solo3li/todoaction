from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Todo

@login_required
def todo_list(request):
    todos = Todo.objects.filter(user=request.user).order_by('-created_at')
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Todo.objects.create(user=request.user, title=title)
        return redirect('todo_list')
    return render(request, 'todos/todo_list.html', {'todos': todos})

@login_required
def toggle_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')

@login_required
def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.delete()
    return redirect('todo_list')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('todo_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
