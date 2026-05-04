from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import User
from .models import Todo
from django import forms
import random

def send_otp_email(request, user):
    otp = str(random.randint(100000, 999999))
    request.session['pre_otp_user_id'] = user.pk
    request.session['otp_code'] = otp
    
    subject = 'Your Verification Code'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = user.email
    
    # Load HTML template
    html_content = render_to_string('todos/email_otp.html', {'otp': otp, 'user': user})
    text_content = strip_tags(html_content)
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        send_otp_email(self.request, user)
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
            if 'pre_otp_user_id' in request.session:
                del request.session['pre_otp_user_id']
            if 'otp_code' in request.session:
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

class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_otp_email(request, user)
            return redirect('verify_otp')
    else:
        form = UserSignupForm()
    return render(request, 'registration/signup.html', {'form': form})
