from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.urls import reverse
from .models import User
from projects.models import Project
from .forms import LoginForm, RegisterForm, UpdateForm

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('projects:home')
        else:
            form.add_error(field=None, error='Email ou senha inválidos')
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
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        confirmed_password = form.cleaned_data.get('confirmed_password')
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


def user_detail(request, id):
    user = get_object_or_404(User, id=id)
    user_projects = Project.objects.filter(author=user, is_approved=True)
    owner = False
    if request.user.is_authenticated and request.user.id == id:
        owner = True
    return render(
        request,
        'users/pages/user_detail.html',
        context={
            'user': user,
            'projects': user_projects,
            'owner': owner
        }
    )


def user_update(request, id):
    if request.user.is_authenticated and request.user.id == id:
        user = get_object_or_404(User, id=id)
        if request.method == 'POST':
            form = UpdateForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                new_password = form.cleaned_data.get('new_password')

                check = check_password(password, user.password)
                if not check:
                    form.add_error(field='password', error='Senha atual incorreta')
                exists = User.objects.filter(email=email).exists()
                if exists and email != user.email:
                     form.add_error(
                        field='email',
                        error='Este email já está em uso'
                    )

                if check and not exists:
                    update_fields = []
                    if username != user.username:
                        user.username = username
                        update_fields.append('username')
                    if email != user.email:
                        user.email = email
                        update_fields.append('email')
                    if new_password:
                        user.password = make_password(new_password)
                        update_fields.append('password')
                        user.save(update_fields=update_fields)
                        return redirect('users:login')
                    user.save(update_fields=update_fields)
                    return redirect(
                            reverse('users:user_detail', kwargs={'id': user.id})
                    )
        else:
            data = {
                'username': user.username,
                'email': user.email,
            }
            form = UpdateForm(initial=data)
        return render(
            request,
            'users/pages/user_update.html',
            context={
                'form': form,
                'id': user.id
            }
        )
    return redirect('projects:home')
