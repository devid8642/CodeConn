from django.forms import ModelForm

from .models import Project, Comment


class ProjectForm(ModelForm):
    class Meta:
        model = Project

        fields = ('title', 'description', 'explanatory_text')


class CommentForm(ModelForm):
    class Meta:
        model = Comment

        fields = ('comment',)
