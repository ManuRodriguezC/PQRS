# Generated by Django 4.2.16 on 2024-11-26 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_responsepqrs'),
    ]

    operations = [
        migrations.AddField(
            model_name='pqrs',
            name='dateResponse',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]