from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404

from .models import ProjectIdea
from .forms import IdeasForm


def projects_ideas(request):
    all_ideas = ProjectIdea.objects.all().order_by('-id')
    backend = []
    frontend = []
    fullstack = []

    for idea in all_ideas:
        if idea.stack == '3':
            fullstack.append(idea)
        elif idea.stack == '1':
            backend.append(idea)
        else:
            frontend.append(idea)

    return render(
        request,
        'projects_ideas.html',
        context={
            'backend': backend,
            'frontend': frontend,
            'fullstack': fullstack,
        }
    )


def idea_detail(request, pk):
    idea = get_object_or_404(ProjectIdea, pk=pk)

    return render(
        request,
        'idea_detail.html',
        context={
            'idea': idea
        }
    )


@login_required(login_url='users:login', redirect_field_name='next')
def ideas_admin(request):
    if request.user.is_staff:
        all_ideas = ProjectIdea.objects.all().order_by('-id')

        form = IdeasForm(request.POST or None)

        if form.is_valid():
            idea = form.save(commit=False)

            idea.save()

            return redirect('ideas:ideas_admin')

    else:
        return redirect('projects:home')

    return render(
        request,
        'ideas_admin.html',
        context={
            'all_ideas': all_ideas,
            'form': form,
        }
    )


def idea_delete(request):
    if not request.POST:
        raise Http404

    idea_id = request.POST.get('idea_id')
    idea = get_object_or_404(
        ProjectIdea,
        id=idea_id,
    )

    messages.error(request, 'Ideia deletada com sucesso!')
    idea.delete()

    return redirect('ideas:ideas_admin')
