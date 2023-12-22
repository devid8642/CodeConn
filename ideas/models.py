from django.db import models

STACK_CHOICES = (('1', 'Backend'), ('2', 'Frontend'), ('3', 'Fullstack'))

LEVEL_CHOICES = (('1', 'Fácil'), ('2', 'Médio'), ('3', 'Difícil'))


class ProjectIdea(models.Model):
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

    class Meta:
        db_table = 'projects_ideas'
        verbose_name = 'Project Idea'
        verbose_name_plural = 'Projects Ideas'
