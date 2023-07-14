from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.http import Http404

from .forms import (
    LoginForm, RegisterForm, UpdateForm, ProjectsDateForm
)
from utils.email_sending import activate_email
from .tokens import account_activation_token
from projects.models import Project
from .models import User, ProjectsDate
from datetime import datetime


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


def activate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except:  # noqa
        user = None

    if user and account_activation_token.check_token(
        user, token
    ):
        user.is_active = True
        user.save()

        messages.success(request, 'Sua conta foi ativada com sucesso!')
        return redirect('users:login')

    else:
        messages.error(request, 'Não foi possível ativar sua conta!')

    return redirect('users:login')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)

            if settings.EMAIL_CONFIRMATION:
                user.is_active = False
                user.save()
                activate_email(request, user, user.email)
            else:
                user.save()
                messages.success(request, 'Você foi registrado com sucesso!')

                return redirect('projects:home')
    else:
        form = RegisterForm()

    return render(
        request,
        'auth/pages/register.html',
        context={
            'form': form
        }
    )


@login_required(login_url='users:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Não foi possível fazer o logout!')

        return redirect('projects:home')

    if request.POST.get('user') != request.user.email:
        messages.error(request, 'Usuário inválido!')

        return redirect('projects:home')

    logout(request)

    return redirect('projects:home')


def user_detail(request, id):
    user = get_object_or_404(User, id=id)

    if request.user == user:
        user_projects = Project.objects.filter(author=user)
    else:
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
            form = UpdateForm(
                request.POST, request.FILES,
                instance=user
            )
            if form.is_valid():
                user = form.save(commit=False)
                new_password = form.cleaned_data.get('new_password')

                if new_password:
                    user.password = make_password(new_password)
                    user.save()
                    return redirect('users:login')

                user.save()
                
                return redirect(
                    reverse('users:user_detail', kwargs={'id': user.id})
                )
        else:
            form = UpdateForm(instance=user)
        return render(
            request,
            'users/pages/user_update.html',
            context={
                'form': form,
                'id': user.id
            }
        )
    return redirect('projects:home')


@login_required(login_url='users:login', redirect_field_name='next')
def admin_dashboard(request):
    if request.user.is_staff:
        users = User.objects.all()
        date = ProjectsDate.get_solo()
        delivered_projects = []
        expired_users = []
        non_approved = Project.objects.filter(
            is_approved=False,
        )
        non_approved_count = non_approved.count()

        form = ProjectsDateForm(
            request.POST or None,
            instance=date,
        )

        if form.is_valid():
            date = form.save(commit=False)
            date.end_date = datetime(
                year=date.end_date.year,
                month=date.end_date.month,
                day=date.end_date.day,
                hour=23,
                minute=59,
                second=59
            )
            date.save()
            return redirect('users:admin_dashboard')

        for user in users:
            project = Project.objects.filter(
                author=user, is_approved=True
            ).last()

            if date.start_date and date.end_date != 'None':
                if project and (
                    project.created_at >= date.start_date and
                    project.created_at <= date.end_date
                ):
                    delivered_projects.append(project)

                else:
                    expired_users.append(user)

    else:
        return redirect('projects:home')

    return render(
        request,
        'users/pages/admin_dashboard.html',
        context={
            'delivered_projects': delivered_projects,
            'expired_users': expired_users,
            'form': form,
            'date': date,
            'non_approved': non_approved,
            'non_approved_count': non_approved_count,
        }
    )
