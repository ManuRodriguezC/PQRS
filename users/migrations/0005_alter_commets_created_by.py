# Generated by Django 4.2.16 on 2024-11-11 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_commets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commets',
            name='created_by',
            field=models.CharField(max_length=200),
        ),
    ]