from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from projects.models import Project
from utils.email_sending import activate_email

from .forms import (
    LoginForm,
    ProjectsDateForm,
    RegisterForm,
    UpdateForm,
    UpdatePasswordForm,
)
from .models import ProjectsDate, User
from .tokens import account_activation_token


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

    return render(request, 'auth/pages/login.html', context={'form': form})


def activate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except:  # noqa
        user = None

    if user and account_activation_token.check_token(user, token):
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
            user.set_password(form.cleaned_data.get('password'))

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

    return render(request, 'auth/pages/register.html', context={'form': form})


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
        context={'user': user, 'projects': user_projects, 'owner': owner},
    )


def user_update(request, id):
    if request.user.is_authenticated and request.user.id == id:
        user = get_object_or_404(User, id=id)
        if request.method == 'POST':
            old_email = user.email
            form = UpdateForm(request.POST, request.FILES, instance=user)

            if form.is_valid():
                user = form.save(old_email=old_email)

                if not user.is_active and settings.EMAIL_CONFIRMATION:
                    activate_email(request, user, user.email)

                    return redirect('users:login')

                messages.success(request, 'Perfil editado com sucesso.')
                return redirect(
                    reverse('users:user_detail', kwargs={'id': user.id})
                )
        else:
            form = UpdateForm(instance=user)
        return render(
            request,
            'users/pages/user_update.html',
            context={'form': form, 'id': user.id},  # type: ignore
        )
    return redirect('projects:home')


@login_required(login_url='users:login', redirect_field_name='next')
def user_update_password(request, id):
    if request.user.id == id:
        user = get_object_or_404(User, pk=id)
        form = UpdatePasswordForm(request.POST or None)

        if form.is_valid():
            password = form.cleaned_data.get('password')

            if not check_password(password, user.password):
                form.add_error(
                    field='password', error='Senha atual incorreta.'
                )

            else:
                user.set_password(form.cleaned_data.get('new_password'))
                user.save(update_fields=['password'])
                messages.success(request, 'Senha redefinida com sucesso.')

                return redirect('users:login')

        return render(
            request,
            'users/pages/user_update_password.html',
            context={'form': form},
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
                second=59,
            )
            date.save()
            return redirect('users:admin_dashboard')

        for user in users:
            project = Project.objects.filter(
                author=user, is_approved=True
            ).last()

            if date.start_date and date.end_date != 'None':
                if project and (
                    project.created_at >= date.start_date
                    and project.created_at <= date.end_date  # type: ignore
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
        },
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
