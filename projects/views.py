from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.urls import reverse

from .models import Project
from .forms import ProjectForm


def home(request):
    week_projects = Project.objects.filter(
        is_approved=True,
    )[:4]

    return render(
        request,
        'projects/pages/home.html',
        context={
            'week_projects': week_projects,
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


def project_detail(request, pk):
    project = get_object_or_404(
        Project,
        id=pk,
    )

    return render(
        request,
        'projects/pages/project_detail.html',
        context={
            'project': project,
        }
    )


def project_create(request):
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        project = form.save(commit=False)
        project.author = request.user
        project.is_approved = False

        project.save()

        return redirect(reverse('projects:home'))

    return render(
        request,
        'projects/pages/project_create.html',
        context={
            'form': form,
        }
    )


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

        return redirect(reverse('projects:home'))

    return render(
        request,
        'projects/pages/project_edit.html',
        context={
            'form': form,
            'project': project,
        }
    )


def project_delete(request):
    if not request.POST:
        raise Http404

    project_id = request.POST.get('project_id')
    project = get_object_or_404(
        Project,
        id=project_id,
    )

    project.delete()

    return redirect(reverse('projects:home'))
