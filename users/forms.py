from django import forms
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
        add_attr(self.fields['email'], 'class', 'form-control')
        add_attr(self.fields['email'], 'autofocus', 'autofocus')

        add_attr(self.fields['password'], 'placeholder', 'Digite sua senha')
        add_attr(self.fields['password'], 'class', 'form-control')

class RegisterForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=255)
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput()
    )
    confirmed_password = forms.CharField(
        label='Confirme sua senha',
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = [
            self.fields['username'],
            self.fields['email'],
            self.fields['password'],
            self.fields['confirmed_password']
        ]
        add_attr(self.fields['username'], 'placeholder', 'Usuário')
        add_attr(self.fields['email'], 'placeholder', 'Email')
        add_attr(self.fields['password'], 'placeholder', 'Digite uma senha')
        add_attr(self.fields['confirmed_password'], 'placeholder', 'Confirme sua senha')
        for field in fields:
            add_attr(field, 'class', 'form-control')
