# Generated by Django 4.2.3 on 2023-07-09 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_comment_read'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint', models.TextField(verbose_name='Denúncia')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='complaints',
            field=models.ManyToManyField(blank=True, to='projects.complaint', verbose_name='Denúncias'),
        ),
    ]
