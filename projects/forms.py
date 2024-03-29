from django import forms

from ideas.models import ProjectIdea
from utils.forms_utils import add_attr

from .models import Comment, Project


class ProjectForm(forms.ModelForm):
    is_inspired = forms.ModelChoiceField(
        label='Inspirado em', queryset=None, required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        title = self.fields['title']
        subtitle = self.fields['subtitle']
        explanatory = self.fields['explanatory_text']
        link = self.fields['link']
        image = self.fields['image']
        self.fields['stack'].required = False

        if self.instance:
            self.fields['is_inspired'].queryset = ProjectIdea.objects.all()

        add_attr(image, 'class', 'post-img')
        add_attr(image, 'onchange', 'preview()')
        add_attr(title, 'placeholder', 'Título do seu projeto')
        add_attr(subtitle, 'placeholder', 'Breve descrição do seu projeto')
        add_attr(
            explanatory, 'placeholder', 'Explique e demonstre seu projeto aqui'
        )
        add_attr(link, 'placeholder', 'Link para o seu projeto/repositório')

    class Meta:
        model = Project

        fields = (
            'title',
            'subtitle',
            'link',
            'explanatory_text',
            'is_inspired',
            'stack',
            'image',
        )


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields['comment'], 'placeholder', 'Deixe seu comentário')

    class Meta:
        model = Comment

        fields = ('comment',)
