# Generated by Django 4.2.1 on 2023-07-05 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_alter_project_is_inspired'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='read',
            field=models.BooleanField(default=False, verbose_name='Lido'),
        ),
    ]
