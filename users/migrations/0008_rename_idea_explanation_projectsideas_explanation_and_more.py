# Generated by Django 4.2.1 on 2023-06-24 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_projectsideas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectsideas',
            old_name='idea_explanation',
            new_name='explanation',
        ),
        migrations.RenameField(
            model_name='projectsideas',
            old_name='idea_level',
            new_name='level',
        ),
        migrations.RemoveField(
            model_name='projectsideas',
            name='idea_deadline',
        ),
        migrations.AddField(
            model_name='projectsideas',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='Data final'),
        ),
        migrations.AddField(
            model_name='projectsideas',
            name='start_date',
            field=models.DateTimeField(null=True, verbose_name='Data inicial'),
        ),
    ]