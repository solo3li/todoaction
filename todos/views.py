from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Todo
import random

class CustomLoginView(LoginView):
    def form_valid(self, form):
        # Do not log the user in yet
        user = form.get_user()
        otp = str(random.randint(100000, 999999))
        
        # Store user ID and OTP in session
        self.request.session['pre_otp_user_id'] = user.pk
        self.request.session['otp_code'] = otp
        
        # Send OTP via email
        send_mail(
            'Your Verification Code',
            f'Your verification code is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return redirect('verify_otp')

def verify_otp(request):
    user_id = request.session.get('pre_otp_user_id')
    if not user_id:
        return redirect('login')
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        saved_otp = request.session.get('otp_code')
        
        if entered_otp == saved_otp:
            user = User.objects.get(pk=user_id)
            auth_login(request, user)
            # Clean up session
            del request.session['pre_otp_user_id']
            del request.session['otp_code']
            return redirect('todo_list')
        else:
            return render(request, 'todos/verify_otp.html', {
                'error': 'Invalid OTP. Please try again.'
            })
            
    return render(request, 'todos/verify_otp.html')

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
            auth_login(request, user)
            return redirect('todo_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
