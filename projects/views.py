from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from django.db.models import Q

from .models import Project, Comment
from .forms import ProjectForm, CommentForm
from ideas.models import ProjectIdea
from users.models import ProjectsDate


def home(request):
    date = ProjectsDate.get_solo()
    week_projects = []
    projects = Project.objects.filter(
        is_approved=True,
    )
    ideas = ProjectIdea.objects.all().order_by('-id')[:4]

    if date.start_date and date.end_date != 'None':
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
            'ideas': ideas,
        }
    )


def all_projects(request):
    idea = request.GET.get('idea')
    idea_name = request.GET.get('idea_name')

    if idea:
        projects = Project.objects.filter(
            is_approved=True,
            is_inspired=idea,
        )
        idea_title = f'baseados em: {idea_name}'

    else:
        projects = Project.objects.filter(
            is_approved=True,
        )
        idea_title = ''

    return render(
        request,
        'projects/pages/all_projects.html',
        context={
            'projects': projects,
            'idea_title': idea_title,
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
            Q(author__username__icontains=search_term) |
            Q(stack__icontains=search_term) |
            Q(is_inspired__idea__icontains=search_term)
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
    project = get_object_or_404(Project, id=pk)

    if request.user == project.author:
        project = get_object_or_404(Project, id=pk)

    else:
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
def comment_notification(request):
    if not request.POST:
        raise Http404

    comment_id = int(request.POST.get('comment_id'))

    comment = get_object_or_404(
        Comment,
        id=comment_id,
    )
    comment.read = True

    comment.save()

    return redirect(
        reverse('projects:project_detail', kwargs={'pk': comment.project.id})
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
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)

        form.fields['stack'].initial = request.GET.get('stack')
        form.fields['is_inspired'].initial = request.GET.get('is_inspired')
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.is_approved = False

            project.save()
            messages.success(
                request,
                'Seu projeto foi criado com sucesso e passará por uma avaliação antes de ser aprovado!'
            )

            return redirect(reverse(
                'users:user_detail', kwargs={'id': request.user.id}
            ))
    else:
        form = ProjectForm()

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
        author=request.user,
    )
    if request.method == 'POST':
        form = ProjectForm(
            request.POST, request.FILES,
            instance=project
        )
        if form.is_valid():
            project = form.save(commit=False)
            project.is_approved = False
            project.save()

            messages.success(request, f'Projeto "{project.title}" editado!')

            return redirect(
                reverse('users:user_detail', kwargs={'id': project.author.id})
            )
    else:
        form = ProjectForm(instance=project)

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
