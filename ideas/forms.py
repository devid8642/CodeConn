from django import forms
from .models import ProjectIdea
from utils.forms_utils import add_attr

class IdeasForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        idea = self.fields['idea']
        explanation = self.fields['explanation']

        add_attr(idea, 'placeholder', 'Ideia de projeto')
        add_attr(explanation, 'placeholder', 'Explicação da ideia')

    class Meta:
        model = ProjectIdea

        fields = ('idea', 'level', 'stack', 'explanation')
