# Generated by Django 4.2.4 on 2023-08-30 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_avatar_url'),
        ('chat', '0003_rename_team_group'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Member',
            new_name='ChatMember',
        ),
    ]
