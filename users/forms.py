from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from utils.forms_utils import add_attr

from .models import ProjectsDate, User


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email', max_length=255, widget=forms.TextInput()
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
            'profile_photo',
            'username',
            'email',
            'linkedin',
            'github',
            'password',
        )

    email = forms.EmailField(
        label='Email', max_length=255, help_text='O email precisa ser válido.'
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(),
        help_text="""
        A senha deve ter no mínimo 8 caracteres e conter letras e números.
        """,
    )
    confirmed_password = forms.CharField(
        label='Confirme sua senha', widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields['username'], 'placeholder', 'Seu nome de usuário')
        add_attr(self.fields['email'], 'placeholder', 'Ex: user@email.com')
        add_attr(self.fields['profile_photo'], 'class', 'profile-img')
        add_attr(self.fields['profile_photo'], 'onchange', 'preview()')
        add_attr(
            self.fields['linkedin'],
            'placeholder',
            'Ex: https://linkedin.com/in/username',
        )
        add_attr(
            self.fields['github'],
            'placeholder',
            'Ex: https://github.com/username',
        )

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
            'profile_photo',
            'username',
            'email',
            'linkedin',
            'github',
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

    def save(self, old_email, commit=True):
        user = super().save(commit=False)

        if user.email != old_email:
            user.is_active = False

        if commit:
            user.save()

        return user


class UpdatePasswordForm(forms.Form):
    password = forms.CharField(
        label='Senha atual', widget=forms.PasswordInput()
    )
    new_password = forms.CharField(
        label='Nova senha',
        widget=forms.PasswordInput(),
        help_text="""
        A senha deve ter no mínimo 8 caracteres e conter letras e números.
        """,
    )

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
                'type': 'date',
                'placeholder': 'yyyy-mm-dd (DOB)',
            }
        )
        self.fields['end_date'].widget = forms.widgets.DateTimeInput(
            attrs={
                'type': 'date',
                'placeholder': 'yyyy-mm-dd (DOB)',
            }
        )

    class Meta:
        model = ProjectsDate

        fields = ('start_date', 'end_date')
