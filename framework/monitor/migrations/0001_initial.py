# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitorScene', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instance_id', models.PositiveIntegerField(verbose_name='\u4f5c\u4e1a\u5b9e\u5217ID')),
                ('status', models.PositiveIntegerField(verbose_name='\u8282\u70b9\u72b6\u6001')),
                ('test_flag', models.PositiveIntegerField(verbose_name='\u6d4b\u8bd5\u6807\u8bc6')),
                ('start_time', models.DateTimeField(verbose_name='\u5f00\u59cb\u65f6\u95f4')),
            ],
            options={
                'db_table': 'td_flow_instance',
                'verbose_name': '\u6d41\u7a0b\u5b9e\u5217\u8868',
                'verbose_name_plural': '\u6d41\u7a0b\u5b9e\u5217\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instance_id', models.PositiveIntegerField(verbose_name='\u4f5c\u4e1a\u5b9e\u5217ID')),
                ('status', models.PositiveIntegerField(verbose_name='\u4f5c\u4e1a\u72b6\u6001')),
                ('test_flag', models.PositiveIntegerField(verbose_name='\u6d4b\u8bd5\u6807\u8bc6')),
                ('start_time', models.DateTimeField(verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('job_log', models.CharField(max_length=500, verbose_name='\u4f5c\u4e1a\u65e5\u5fd7')),
            ],
            options={
                'db_table': 'td_job_instance',
                'verbose_name': '\u4f5c\u4e1a\u5b9e\u5217\u8868',
                'verbose_name_plural': '\u4f5c\u4e1a\u5b9e\u5217\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monitor_name', models.CharField(unique=True, max_length=50, verbose_name='\u76d1\u63a7\u9879\u540d\u79f0')),
                ('monitor_type', models.PositiveIntegerField(verbose_name='\u76d1\u63a7\u9879\u7c7b\u578b')),
                ('jion_id', models.PositiveIntegerField(unique=True, verbose_name='\u5173\u8054ID')),
                ('gather_rule', models.CharField(max_length=50, verbose_name='\u91c7\u96c6\u89c4\u5219')),
                ('gather_params', models.CharField(max_length=500, verbose_name='\u91c7\u96c6\u53c2\u6570')),
                ('params', models.CharField(max_length=500, verbose_name='\u76d1\u63a7\u53c2\u6570')),
                ('width', models.PositiveIntegerField(verbose_name='\u5bbd')),
                ('height', models.PositiveIntegerField(verbose_name='\u9ad8')),
                ('font_size', models.PositiveIntegerField(verbose_name='\u5b57\u4f53\u5927\u5c0f')),
                ('period', models.PositiveIntegerField(verbose_name='\u91c7\u96c6\u5468\u671f')),
                ('start_time', models.TimeField(verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('end_time', models.TimeField(verbose_name='\u7ed3\u675f\u65f6\u95f4')),
                ('create_time', models.TimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('creator', models.CharField(max_length=10, verbose_name='\u521b\u5efa\u4eba')),
                ('editor', models.CharField(max_length=10, verbose_name='\u7f16\u8f91\u4eba')),
                ('edit_time', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('status', models.PositiveIntegerField(verbose_name='\u76d1\u63a7\u72b6\u6001')),
                ('contents', models.CharField(max_length=500, verbose_name='\u663e\u793a\u5185\u5bb9')),
            ],
            options={
                'db_table': 'tb_monitor_item',
                'verbose_name': '\u76d1\u63a7\u9879\u4fe1\u606f\u8868',
                'verbose_name_plural': '\u76d1\u63a7\u9879\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='scene_monitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.PositiveIntegerField(verbose_name='x\u5750\u6807')),
                ('y', models.PositiveIntegerField(verbose_name='y\u5750\u6807')),
                ('scale', models.PositiveIntegerField(verbose_name='\u6bd4\u4f8b')),
                ('score', models.PositiveIntegerField(verbose_name='\u6253\u5206')),
                ('order', models.PositiveIntegerField(verbose_name='\u6392\u5e8f')),
                ('item', models.ForeignKey(to='monitor.Monitor')),
                ('pos', models.ForeignKey(to='monitorScene.Scene')),
            ],
            options={
                'db_table': 'tl_scene_monitor',
                'verbose_name': '\u573a\u666f\u76d1\u63a7\u9879',
                'verbose_name_plural': '\u573a\u666f\u76d1\u63a7\u9879',
            },
        ),
        migrations.AddField(
            model_name='job',
            name='job_id',
            field=models.OneToOneField(to='monitor.Monitor', to_field=b'jion_id'),
        ),
        migrations.AddField(
            model_name='flow',
            name='flow_id',
            field=models.OneToOneField(to='monitor.Monitor', to_field=b'jion_id'),
        ),
    ]
