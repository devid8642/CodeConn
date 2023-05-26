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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['email'], 'placeholder', 'Email')
        add_attr(self.fields['password'], 'placeholder', 'Digite sua senha')

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['username'], 'placeholder', 'Usuário')
        add_attr(self.fields['email'], 'placeholder', 'Email')
        add_attr(self.fields['password'], 'placeholder', 'Digite uma senha')
        add_attr(self.fields['confirmed_password'], 'placeholder', 'Confirme sua senha')

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
