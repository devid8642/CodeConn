# Generated by Django 4.2.1 on 2023-06-18 17:21

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_alter_project_explanatory_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='explanatory_text',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Texto de explicação'),
        ),
    ]