from django.forms import ModelForm

from .models import Project, Comment
from utils.forms_utils import add_attr


class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        title = self.fields['title']
        description = self.fields['description']
        explanatory = self.fields['explanatory_text']

        add_attr(title, 'placeholder', 'Título do projeto')
        add_attr(description, 'placeholder', 'Descreva seu projeto')
        add_attr(explanatory, 'placeholder', 'Sobre o seu projeto')

    class Meta:
        model = Project

        fields = ('title', 'description', 'explanatory_text')


class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields['comment'], 'placeholder', 'Deixe seu comentário')

    class Meta:
        model = Comment

        fields = ('comment',)
