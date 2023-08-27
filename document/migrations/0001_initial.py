# Generated by Django 4.2.4 on 2023-08-27 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prototype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='标题')),
                ('content', models.TextField(default='', verbose_name='')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='最近修改时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否已删除')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='team.team', verbose_name='原型所属团队')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.user', verbose_name='创建者')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='标题')),
                ('content', models.TextField(verbose_name='文档内容')),
                ('url', models.URLField(null=True, verbose_name='不可编辑文档链接')),
                ('url_editable', models.URLField(null=True, verbose_name='可编辑链接')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='最近修改时间')),
                ('is_locked', models.IntegerField(default=False, verbose_name='文件锁')),
                ('is_locked', models.IntegerField(default=False, verbose_name='文件锁')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否被删除')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='team.team', verbose_name='所属团队')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.user', verbose_name='创建者')),
            ],
        ),
    ]
