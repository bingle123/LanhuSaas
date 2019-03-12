# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Createtmp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('tmpdate', models.TextField(max_length=10000, verbose_name='\u6570\u636e')),
            ],
        ),
        migrations.CreateModel(
            name='position_scene',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position_id', models.PositiveIntegerField(verbose_name='\u5c97\u4f4did')),
            ],
            options={
                'db_table': 'tl_position_scene',
                'verbose_name': '\u5c97\u4f4d\u4e0e\u573a\u666f\u5173\u7cfb\u8868',
                'verbose_name_plural': '\u5c97\u4f4d\u4e0e\u573a\u666f\u5173\u7cfb\u8868',
            },
        ),
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scene_name', models.CharField(max_length=50, verbose_name='\u573a\u666f\u540d\u79f0')),
                ('scene_startTime', models.TimeField(verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('scene_endTime', models.TimeField(verbose_name='\u7ed3\u675f\u65f6\u95f4')),
                ('scene_creator', models.CharField(max_length=50, verbose_name='\u521b\u5efa\u4eba')),
                ('scene_creator_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('scene_editor', models.CharField(max_length=50, verbose_name='\u7f16\u8f91\u4eba')),
                ('scene_editor_time', models.DateTimeField(auto_now=True, verbose_name='\u7f16\u8f91\u65f6\u95f4')),
                ('scene_area', models.IntegerField(verbose_name='\u573a\u666f\u65e5\u5386\u5730\u533a')),
            ],
            options={
                'db_table': 'tb_monitor_scene',
                'verbose_name': '\u573a\u666f\u4fe1\u606f',
                'verbose_name_plural': '\u573a\u666f\u4fe1\u606f',
            },
        ),
        migrations.AddField(
            model_name='position_scene',
            name='scene',
            field=models.ForeignKey(related_name='scene_id', to='monitorScene.Scene'),
        ),
    ]
