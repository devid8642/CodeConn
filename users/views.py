from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . models import User

def loginn(request):
    if request.method == 'GET':
        return render(request, 'auth/pages/login.html')
    else:
        if 'email' in request.POST and 'password' in request.POST:
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('projects:home')
        # Redirect indicating error message
        return render(request, 'auth/pages/login.html')

def register(request):
    if request.method == 'GET':
        return render(request, 'auth/pages/register.html')
    else:
        expected_fields = [
            'username',
            'email',
            'password',
            'confirmed_password'
        ]
        for field in expected_fields:
            if field not in request.POST:
                # Redirect indicating error message
                return render(request, 'auth/pages/register.html')
        if request.POST['password'] != request.POST['confirmed_password']:
            # Redirect indicating error message
            return render(request, 'auth/pages/register.html')
        try:
            User.objects.get(email = request.POST['email'])
        except User.DoesNotExist:
            User.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password']
            )
            return redirect('users:login')
        else:
            # Redirect indicating error message
            return render(request, 'auth/pages/register.html')

def logoutt(request):
    logout(request)
    return redirect('projects:home')