from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User
from .forms import LoginForm, RegisterForm

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('projects:home')
    return render(
        request,
        'auth/pages/login.html',
        context={
            'form': form
        }
    )


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmed_password = request.POST.get('confirmed_password')
        if password == confirmed_password:
            try:
                User.objects.get(email = email)
            except User.DoesNotExist:
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                return redirect('users:login')
    return render(
        request,
        'auth/pages/register.html',
        context={
            'form': form
        }
    )

def logout_view(request):
    logout(request)
    return redirect('projects:home')
