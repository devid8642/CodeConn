from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import User, ProjectsDate
from utils.forms_utils import add_attr


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=255,
        widget=forms.TextInput()
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields['email'], 'placeholder', 'Ex: user@email.com')
        add_attr(self.fields['email'], 'autofocus', 'True')
        add_attr(self.fields['password'], 'placeholder', 'Sua senha')


class RegisterForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=255)
    email = forms.EmailField(
        label='Email',
        max_length=255,
        widget=forms.TextInput()
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(),
    )
    confirmed_password = forms.CharField(
        label='Confirme sua senha',
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields['username'], 'placeholder', 'Seu nome de usuário')
        add_attr(self.fields['email'], 'placeholder', 'Ex: user@email.com')
        add_attr(self.fields['password'], 'placeholder', 'Sua senha')
        add_attr(
            self.fields['confirmed_password'],
            'placeholder',
            'Confirme sua senha',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            exists = User.objects.filter(email=email).exists()
            if exists:
                raise ValidationError('Já existe um usuário com este email')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmed_password = cleaned_data.get('confirmed_password')
        if password and confirmed_password:
            if password != confirmed_password:
                raise ValidationError('Você digitou senhas diferentes')


class UpdateForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=255)
    email = forms.EmailField(
        label='Email',
        max_length=255,
        widget=forms.TextInput()
    )
    linkedin = forms.URLField(
        label='Linkedin',
        required=False,
        widget=forms.TextInput()
    )
    github = forms.URLField(
        label='Github',
        required=False,
        widget=forms.TextInput()
    )
    password = forms.CharField(
        label='Senha atual',
        widget=forms.PasswordInput()
    )
    new_password = forms.CharField(
        label='Nova senha',
        widget=forms.PasswordInput(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            add_attr(self.fields[field], 'class', 'formulario-input')

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            validate_password(new_password)
        return new_password


class ProjectsDateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].widget = forms.widgets.DateTimeInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
            }
        )
        self.fields['end_date'].widget = forms.widgets.DateTimeInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
            }
        )

    class Meta:
        model = ProjectsDate

        fields = ('start_date', 'end_date')
