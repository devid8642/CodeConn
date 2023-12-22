from ckeditor.fields import RichTextField
from django.db import models

from ideas.models import ProjectIdea
from users.models import User
from utils.image import resize_image

STACKS = (
    ('1', 'Backend'),
    ('2', 'Frontend'),
    ('3', 'Fullstack'),
)


class Project(models.Model):
    title = models.CharField('Título', max_length=50)
    subtitle = models.CharField('Subtítulo', max_length=100)
    explanatory_text = RichTextField(
        'Texto de explicação', blank=True, null=True
    )
    author = models.ForeignKey(
        User, verbose_name='Autor', on_delete=models.SET_NULL, null=True
    )
    link = models.URLField('Link do projeto', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField('Publicado', default=True)
    is_inspired = models.ForeignKey(
        ProjectIdea,
        verbose_name='Inspirado em',
        on_delete=models.SET_NULL,
        null=True,
    )
    stack = models.CharField(
        'Stack utilizada', max_length=255, null=True, choices=STACKS
    )
    complaints = models.IntegerField(
        'Denúncias',
        default=0,
    )
    complaints_notifications = models.IntegerField(
        'Notificação de denúncia',
        default=0,
    )
    image = models.ImageField(
        'Imagem do projeto',
        upload_to='projects_images/',
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        saved = super().save(*args, **kwargs)

        if self.image:
            try:
                resize_image(self.image, new_width=800)
            except FileNotFoundError:
                pass

        return saved

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
        User,
        on_delete=models.SET_NULL,
        related_name='comment_user',
        null=True,
        default='',
    )
    comment = models.TextField('Comentário')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read = models.BooleanField('Lido', default=False)

    def __str__(self):
        return f'Comment {self.id}'

    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']
