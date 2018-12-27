# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='unit_administration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unit_name', models.CharField(unique=True, max_length=200, verbose_name='\u5355\u5143\u540d\u79f0')),
                ('unit_type', models.CharField(max_length=200, verbose_name='\u5355\u5143\u7c7b\u578b')),
                ('editor', models.CharField(max_length=200, verbose_name='\u7f16\u8f91\u4eba')),
                ('edit_time', models.CharField(max_length=200, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('font_size', models.PositiveIntegerField(verbose_name='\u5b57\u53f7')),
                ('hight', models.PositiveIntegerField(verbose_name='\u9ad8')),
                ('wide', models.PositiveIntegerField(verbose_name='\u5bbd')),
                ('content', models.CharField(max_length=2000, verbose_name='\u663e\u793a\u5185\u5bb9')),
                ('data_source', models.CharField(max_length=200, verbose_name='\u6570\u636e\u6765\u6e90')),
                ('time_slot', models.CharField(max_length=200, verbose_name='\u65f6\u95f4\u6bb5')),
                ('time_interval', models.PositiveIntegerField(verbose_name='\u95f4\u9694\u65f6\u95f4\u79d2')),
                ('template', models.CharField(max_length=200, verbose_name='\u6570\u636e\u5e93\u548c\u6a21\u677f')),
                ('chart_type', models.CharField(max_length=200, verbose_name='\u56fe\u8868\u7c7b\u578b')),
                ('parameter', models.CharField(max_length=5000, verbose_name='\u6587\u4ef6\u5185\u5bb9\u3001\u811a\u672c\u53c2\u6570\u3001\u6a21\u677f\u53c2\u6570')),
            ],
            options={
                'verbose_name': '\u5355\u5143\u4fe1\u606f',
                'verbose_name_plural': '\u5355\u5143\u4fe1\u606f',
            },
        ),
    ]
