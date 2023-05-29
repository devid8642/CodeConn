from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import User

def add_attr(field, attr, value):
    field.widget.attrs.update(
        {
            attr: value
        }
    )

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(),
    )

class RegisterForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=255)
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(),
    )
    confirmed_password = forms.CharField(
        label='Confirme sua senha',
        widget=forms.PasswordInput()
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
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(
        label='Senha atual',
        widget=forms.PasswordInput()
    )
    new_password = forms.CharField(
        label='Nova senha',
        widget=forms.PasswordInput(),
        required=False
    )

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            validate_password(new_password)
        return new_password
