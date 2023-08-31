# Generated by Django 3.2.5 on 2023-08-31 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_alter_group_is_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='forwarded_from',
            field=models.ManyToManyField(blank=True, related_name='_chat_chatmessage_forwarded_from_+', to='chat.ChatMessage'),
        ),
    ]
