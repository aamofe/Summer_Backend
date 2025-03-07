# Generated by Django 4.2.4 on 2023-08-30 03:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_avatar_url'),
        ('team', '0003_auto_20230830_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_team_user', to='user.user', verbose_name='成员'),
        ),
        migrations.AlterField(
            model_name='team',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_member_user', to='user.user', verbose_name='创建者'),
        ),
    ]
