# Generated by Django 4.2.3 on 2023-07-13 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_comment_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='projects_images/'),
        ),
    ]
