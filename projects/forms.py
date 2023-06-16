from django import forms

from .models import Project, Comment
from utils.forms_utils import add_attr


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        title = self.fields['title']
        subtitle = self.fields['subtitle']
        explanatory = self.fields['explanatory_text']
        link = self.fields['link']

        add_attr(title, 'placeholder', 'Título do seu projeto')
        add_attr(subtitle, 'placeholder', 'Breve descrição')
        add_attr(
            explanatory, 'placeholder', 'Explique e demonstre seu projeto aqui'
        )
        add_attr(link, 'placeholder', 'Link para o seu projeto/repositório')

    class Meta:
        model = Project

        fields = ('title', 'subtitle', 'link', 'explanatory_text')


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields['comment'], 'placeholder', 'Deixe seu comentário')

    class Meta:
        model = Comment

        fields = ('comment',)
