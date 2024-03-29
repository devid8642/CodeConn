# Generated by Django 4.2.3 on 2023-07-17 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_alter_project_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='complaints',
            field=models.IntegerField(default=0, verbose_name='Denúncias'),
        ),
        migrations.AlterField(
            model_name='project',
            name='complaints_notifications',
            field=models.IntegerField(default=0, verbose_name='Notificação de denúncia'),
        ),
    ]
