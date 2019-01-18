# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicUnit',
            fields=[
                ('unit_id', models.PositiveIntegerField(serialize=False, verbose_name='\u5355\u5143id', primary_key=True)),
                ('contents', models.CharField(max_length=100, verbose_name='\u663e\u793a\u5185\u5bb9')),
                ('sql_file_interface', models.CharField(max_length=20, verbose_name='\u6570\u636e\u6765\u6e90')),
                ('sql', models.CharField(max_length=20, verbose_name='\u8fde\u63a5\u6570\u636e\u5e93')),
                ('rules', models.CharField(max_length=100, verbose_name='\u91c7\u96c6\u89c4\u5219')),
                ('server', models.CharField(max_length=20, verbose_name='\u670d\u52a1\u5668')),
                ('file', models.CharField(max_length=50, verbose_name='\u6587\u4ef6\u8def\u5f84')),
                ('urls', models.CharField(max_length=100, verbose_name='\u63a5\u53e3url')),
                ('param', models.CharField(max_length=20, verbose_name='\u63a5\u53e3\u53c2\u6570')),
            ],
        ),
        migrations.CreateModel(
            name='ChartUnit',
            fields=[
                ('unit_id', models.PositiveIntegerField(serialize=False, verbose_name='\u5355\u5143id', primary_key=True)),
                ('contents', models.CharField(max_length=100, verbose_name='\u663e\u793a\u5185\u5bb9')),
                ('chart_type', models.CharField(max_length=20, verbose_name='\u56fe\u8868\u7c7b\u578b')),
                ('sql', models.CharField(max_length=20, verbose_name='\u8fde\u63a5\u6570\u636e\u5e93')),
                ('rules', models.CharField(max_length=100, verbose_name='\u91c7\u96c6\u89c4\u5219')),
            ],
        ),
        migrations.CreateModel(
            name='Common',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unit_name', models.CharField(unique=True, max_length=40, verbose_name='\u5355\u5143\u540d\u79f0')),
                ('unit_type', models.CharField(max_length=20, verbose_name='\u5355\u5143\u7c7b\u578b')),
                ('editor', models.CharField(max_length=20, verbose_name='\u7f16\u8f91\u4eba')),
                ('edit_time', models.DateTimeField(verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('font_size', models.PositiveIntegerField(verbose_name='\u5b57\u53f7')),
                ('height', models.PositiveIntegerField(verbose_name='\u9ad8')),
                ('wide', models.PositiveIntegerField(verbose_name='\u5bbd')),
                ('start_time', models.DateTimeField(verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('end_time', models.DateTimeField(verbose_name='\u7ed3\u675f\u65f6\u95f4')),
                ('cycle', models.PositiveIntegerField(verbose_name='\u91c7\u96c6\u5468\u671f')),
            ],
        ),
        migrations.CreateModel(
            name='FlowUnit',
            fields=[
                ('unit_id', models.PositiveIntegerField(serialize=False, verbose_name='\u5355\u5143id', primary_key=True)),
                ('flow_mould', models.CharField(max_length=50, verbose_name='\u6d41\u7a0b\u6a21\u677f')),
                ('param', models.CharField(max_length=20, verbose_name='\u6a21\u677f\u53c2\u6570')),
                ('node', models.CharField(max_length=20, verbose_name='\u8282\u70b9\u540d\u79f0')),
            ],
        ),
        migrations.CreateModel(
            name='JobUnit',
            fields=[
                ('unit_id', models.PositiveIntegerField(serialize=False, verbose_name='\u5355\u5143id', primary_key=True)),
                ('contents', models.CharField(max_length=100, verbose_name='\u663e\u793a\u5185\u5bb9')),
                ('job_mould', models.CharField(max_length=50, verbose_name='\u4f5c\u4e1a\u6a21\u677f')),
                ('NODE_KEY', models.CharField(max_length=50, verbose_name='NODE_KEY')),
                ('server', models.CharField(max_length=20, verbose_name='\u6267\u884c\u670d\u52a1\u5668')),
            ],
        ),
        migrations.DeleteModel(
            name='unit_administration',
        ),
    ]
