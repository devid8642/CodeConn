from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)
from solo.models import SingletonModel


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'User {self.id} - {self.email}'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'users'
        ordering = ['id']


class ProjectsDate(SingletonModel):
    start_date = models.DateTimeField('Data inicial', null=True)
    end_date = models.DateTimeField('Data final', null=True)

    def __str__(self):
        return f'Prazo: {self.start_date} - {self.end_date}'

    class Meta:
        db_table = 'prazo'
        verbose_name = 'prazo'


STACK_CHOICES = (
    ('1', 'Backend'),
    ('2', 'Frontend'),
    ('3', 'Fullstack')
)

LEVEL_CHOICES = (
    ('1', 'Fácil'),
    ('2', 'Médio'),
    ('3', 'Difícil')
)


class ProjectsIdeas(models.Model):
    idea = models.CharField('Ideia de projeto', max_length=255)
    level = models.CharField('Nível', max_length=255, choices=LEVEL_CHOICES)
    stack = models.CharField(
        'Stack', max_length=255, null=True, choices=STACK_CHOICES
    )
    explanation = models.TextField('Explicação')
    start_date = models.DateTimeField(
        'Data inicial', null=True, auto_now_add=True
    )

    def __str__(self):
        return self.idea
