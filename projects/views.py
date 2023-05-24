from django.shortcuts import render

from .models import Project


def home(request):
    week_projects = Project.objects.filter(
        is_approved=True,
    )

    return render(
        request,
        'users/pages/home.html',
        context={
            'week_projects': week_projects,
        }
    )


def all_projects(request):
    projects = Project.objects.filter(
        is_approved=True,
    ).order_by('-id')

    return render(
        request,
        'users/pages/all_projects.html',
        context={
            'projects': projects,
        }
    )
