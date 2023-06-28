# Generated by Django 4.2.2 on 2023-06-27 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_project_stack'),
        ('users', '0011_remove_projectsideas_end_date_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProjectsIdeas',
            new_name='ProjectIdea',
        ),
        migrations.AlterModelOptions(
            name='projectidea',
            options={'verbose_name': 'Project Idea', 'verbose_name_plural': 'Projects Ideas'},
        ),
        migrations.AlterModelTable(
            name='projectidea',
            table='projects_ideas',
        ),
    ]