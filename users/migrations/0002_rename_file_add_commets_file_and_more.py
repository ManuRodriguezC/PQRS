# Generated by Django 4.2.16 on 2024-11-19 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commets',
            old_name='file_add',
            new_name='file',
        ),
        migrations.RemoveField(
            model_name='commets',
            name='image_add',
        ),
    ]
