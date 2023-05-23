from django.db import models

from users.models import User


class Project(models.Model):
    title = models.CharField('Título', max_length=50)
    description = models.CharField('Descrição', max_length=100)
    explanatory_text = models.TextField('Texto de explicação')
    author = models.ForeignKey(
        User, verbose_name='Autor', on_delete=models.SET_NULL, null=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField('Publicado', default=False)
