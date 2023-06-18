from django.db import models
from ckeditor.fields import RichTextField

from users.models import User


class Project(models.Model):
    title = models.CharField('Título', max_length=50)
    subtitle = models.CharField('Subtítulo', max_length=100)
    explanatory_text = RichTextField(
        'Texto de explicação', blank=True, null=True
    )
    # explanatory_text = models.TextField('Texto de explicação')
    author = models.ForeignKey(
        User, verbose_name='Autor', on_delete=models.SET_NULL, null=True
    )
    link = models.URLField('Link do projeto', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField('Publicado', default=False)

    def __str__(self):
        return f'Project {self.id} - {self.title}'

    class Meta:
        db_table = 'projects'
        ordering = ['-created_at']


class Comment(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        related_name='comment_user',
        null=True,
        default='',
    )
    comment = models.TextField('Comentário')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment {self.id}'

    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']
