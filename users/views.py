from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

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
                return redirect('/')
        return render(request, 'auth/pages/login.html')
