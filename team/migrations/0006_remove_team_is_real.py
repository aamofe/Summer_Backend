# Generated by Django 3.2.5 on 2023-08-31 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0005_project_deleted_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='is_real',
        ),
    ]
