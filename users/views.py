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
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        linkedin = form.cleaned_data.get('linkedin')
        github = form.cleaned_data.get('github')
        password = form.cleaned_data.get('password')
        form.cleaned_data.get('confirmed_password')

        if settings.EMAIL_CONFIRMATION:
            user = User.objects.create_user(
                username=username,
                email=email,
                linkedin=linkedin,
                github=github,
                password=password,
                is_active=False,
            )
            activate_email(request, user, email)

        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                linkedin=linkedin,
                github=github,
                password=password,
                is_active=True,
            )
            messages.success(request, 'Você foi registrado com sucesso!')

            return redirect('projects:home')

        return redirect('projects:home')

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
            form = UpdateForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                new_password = form.cleaned_data.get('new_password')
                linkedin = form.cleaned_data.get('linkedin')
                github = form.cleaned_data.get('github')

                check = check_password(password, user.password)
                if not check:
                    form.add_error(
                        field='password', error='Senha atual incorreta'
                    )
                exists = User.objects.filter(email=email).exists()
                email_error = False
                if exists and email != user.email:
                    form.add_error(
                        field='email',
                        error='Este email já está em uso'
                    )
                    email_error = True

                if check and not email_error:
                    update_fields = []
                    if username != user.username:
                        user.username = username
                        update_fields.append('username')
                    if email != user.email:
                        user.email = email
                        update_fields.append('email')
                    if linkedin:
                        user.linkedin = linkedin
                        update_fields.append('linkedin')
                    if github:
                        user.github = github
                        update_fields.append('github')
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


@login_required(login_url='users:login', redirect_field_name='next')
def admin_dashboard(request):
    if request.user.is_staff:
        users = User.objects.all()
        date = ProjectsDate.get_solo()
        projects = Project.objects.all()

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
            'projects': projects,
            'delivered_projects': delivered_projects,
            'expired_users': expired_users,
            'form': form,
            'date': date,
            'non_approved': non_approved,
            'non_approved_count': non_approved_count,
        }
    )


@login_required(login_url='users:login', redirect_field_name='next')
def project_block(request):
    if not request.POST:
        raise Http404

    project_id = request.POST.get('project_id')

    project = get_object_or_404(
        Project,
        id=project_id,
    )

    project.is_approved = False

    project.save()

    messages.error(request, f'"{project.title}" foi bloqueado!')

    return redirect('users:admin_dashboard')


@login_required(login_url='users:login', redirect_field_name='next')
def complaints_remove(request):
    if not request.POST:
        raise Http404

    project_id = request.POST.get('project_id')

    project = get_object_or_404(
        Project,
        id=project_id,
    )

    project.complaints = 0
    project.complaints_notifications = 0

    if not project.is_approved:
        project.is_approved = True

    project.save()

    messages.success(
        request, f'Denúncias de "{project.title}" removidas com sucesso!'
    )

    return redirect('users:admin_dashboard')
