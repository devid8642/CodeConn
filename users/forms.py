from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password, make_password
from .models import User, ProjectsDate
from ideas.models import ProjectIdea
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

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'linkedin',
            'github',
            'profile_photo',
            'password'
        )

    email = forms.EmailField(
        label='Email',
        max_length=255,
        help_text='O email precisa ser válido.'
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(),
        help_text='''
        A senha deve ter no mínimo 8 caracteres e conter letras e números. 
        '''
    )
    confirmed_password = forms.CharField(
        label='Confirme sua senha',
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields['username'], 'placeholder', 'Seu nome de usuário')
        add_attr(self.fields['email'], 'placeholder', 'Ex: user@email.com')
        add_attr(self.fields['linkedin'], 'placeholder', 'Ex: https://linkedin.com/in/username')
        add_attr(self.fields['github'], 'placeholder', 'Ex: https://github.com/username')
        if 'password' in self.fields:
            add_attr(self.fields['password'], 'placeholder', 'Sua senha')
        if 'confirmed_password' in self.fields:
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
                raise ValidationError('Já existe um usuário com este email.')
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
                raise ValidationError('Você digitou senhas diferentes.')


class UpdateForm(RegisterForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'linkedin',
            'github',
            'profile_photo',
        )

    password = None
    confirmed_password = None
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email:
            exists = User.objects.filter(email=email).exists()

            if exists and email != self.instance.email:
                raise ValidationError('Este email já está em uso.')
        
        return email
    
    def clean_password(self):
        pass

    def clean(self):
        pass


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
