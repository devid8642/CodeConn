from django import forms

from .models import Project, Comment
from utils.forms_utils import add_attr


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field == 'explanatory_text':
                descricao = '''Descreva a ideia por trás do seu projeto, suas funcionalidadese e se possível adicione links para vídeos ou imagens do projeto.'''
                self.fields[field].widget = forms.Textarea(
                    attrs={'cols': 50, 'rows': 20}
                )
                add_attr(self.fields[field], 'placeholder', descricao)
            add_attr(self.fields[field], 'class', 'formulario-input')

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
