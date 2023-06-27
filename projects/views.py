from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from django.db.models import Q

from .models import Project, Comment
from .forms import ProjectForm, CommentForm
from users.models import ProjectsDate


def home(request):
    date = ProjectsDate.get_solo()
    week_projects = []
    projects = Project.objects.filter(
        is_approved=True,
    )

    for project in projects:
        if project and (
            project.created_at >= date.start_date and
            project.created_at <= date.end_date
        ):
            week_projects.append(project)

    return render(
        request,
        'projects/pages/home.html',
        context={
            'week_projects': week_projects,
            'date': date,
        }
    )


def all_projects(request):
    projects = Project.objects.filter(
        is_approved=True,
    )

    return render(
        request,
        'projects/pages/all_projects.html',
        context={
            'projects': projects,
        }
    )


def project_search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404

    projects = Project.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(subtitle__icontains=search_term) |
            Q(author__username__icontains=search_term)
        ),
        is_approved=True,
    )

    return render(
        request,
        'projects/pages/project_search.html',
        context={
            'projects': projects,
            'search_term': search_term
        }
    )


def project_detail(request, pk):
    project = get_object_or_404(
        Project,
        is_approved=True,
        id=pk,
    )
    comments = Comment.objects.filter(
        project=project,
    ).order_by('-created_at')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.project = project
            comment.author = request.user

            comment.save()

            return redirect(
                reverse('projects:project_detail', kwargs={'pk': pk})
            )

    else:
        comment_form = CommentForm()

    return render(
        request,
        'projects/pages/project_detail.html',
        context={
            'project': project,
            'comments': comments,
            'comment_form': comment_form,
        }
    )


@login_required(login_url='users:login', redirect_field_name='next')
def comment_delete(request):
    if not request.POST:
        raise Http404

    comment_id = request.POST.get('comment-id')
    comment = get_object_or_404(
        Comment,
        author=request.user,
        id=comment_id,
    )
    project_id = comment.project.id
    comment.delete()

    return redirect(
        reverse('projects:project_detail', kwargs={'pk': project_id})
    )


@login_required(login_url='users:login', redirect_field_name='next')
def project_create(request):
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        project = form.save(commit=False)
        project.author = request.user
        project.is_approved = False
        if project.is_inspired:
            project.stack = project.is_inspired.stack

        project.save()
        messages.success(request, 'Projeto criado com sucesso!')

        return redirect(reverse(
            'users:user_detail', kwargs={'id': request.user.id}
        ))

    return render(
        request,
        'projects/pages/project_create.html',
        context={
            'form': form,
        }
    )


@login_required(login_url='users:login', redirect_field_name='next')
def project_edit(request, pk):
    project = get_object_or_404(
        Project,
        id=pk,
    )
    form = ProjectForm(
        request.POST or None,
        instance=project,
    )

    if form.is_valid():
        project = form.save(commit=False)
        project.is_approved = False
        project.save()

        messages.success(request, f'Projeto "{project.title}" editado!')

        return redirect(
            reverse('users:user_detail', kwargs={'id': project.author.id})
        )

    return render(
        request,
        'projects/pages/project_edit.html',
        context={
            'form': form,
            'project': project,
        }
    )


@login_required(login_url='users:login', redirect_field_name='next')
def project_delete(request):
    if not request.POST:
        raise Http404

    project_id = request.POST.get('project_id')
    project = get_object_or_404(
        Project,
        id=project_id,
    )

    messages.error(request, 'Projeto deletado com sucesso!')

    project.delete()

    return redirect(
        reverse('users:user_detail', kwargs={'id': project.author.id})
    )
