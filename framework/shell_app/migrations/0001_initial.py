# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bk_biz_name', models.CharField(max_length=50, verbose_name='\u4e1a\u52a1')),
                ('bk_cloud_name', models.CharField(max_length=200, verbose_name='\u4e91\u533a\u57df')),
                ('bk_biz_id', models.CharField(max_length=16, verbose_name='\u4e1a\u52a1')),
                ('bk_cloud_id', models.CharField(max_length=16, verbose_name='\u4e91\u533a\u57df')),
                ('bk_os_type', models.CharField(default=b'Linux', max_length=64, verbose_name='\u7cfb\u7edf\u7c7b\u578b')),
                ('module_name', models.CharField(default=b'', max_length=64, verbose_name='\u6240\u5c5e\u6a21\u5757', blank=True)),
                ('inner_ip', models.GenericIPAddressField(verbose_name='\u5185\u7f51IP')),
                ('run_time', models.DateTimeField(auto_now_add=True, verbose_name='\u6267\u884c\u65f6\u95f4')),
                ('success', models.BooleanField(default=False, verbose_name='\u6267\u884c\u662f\u5426\u6210\u529f')),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u4fe1\u606f',
                'verbose_name_plural': '\u4e3b\u673a\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='PositionScene',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('staff_position_id', models.IntegerField(verbose_name='\u804c\u5458\u5c97\u4f4dID')),
                ('scene_id', models.IntegerField(verbose_name='\u573a\u666fID')),
            ],
            options={
                'verbose_name': '\u5c97\u4f4d\u4e0e\u573a\u666f\u5173\u7cfb\u8868',
                'verbose_name_plural': '\u5c97\u4f4d\u573a\u666f\u5173\u7cfb\u8868',
            },
        ),
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scene_id', models.IntegerField(verbose_name='\u573a\u666fID')),
                ('scene_name', models.CharField(max_length=64, verbose_name='\u573a\u666f\u540d\u79f0')),
                ('scene_example', models.CharField(max_length=64, verbose_name='\u573a\u666f\u5b9e\u4f8b')),
                ('scene_start_time', models.TimeField(auto_now=True)),
                ('scene_stop_time', models.TimeField(auto_now=True)),
                ('scene_default_time', models.CharField(max_length=64, verbose_name='\u573a\u666f\u505c\u7559\u65f6\u95f4')),
                ('scene_order_id', models.IntegerField(verbose_name='\u573a\u666f\u6392\u5e8fID')),
                ('staff_position_id', models.IntegerField(verbose_name='\u804c\u5458\u5c97\u4f4dID')),
            ],
            options={
                'verbose_name': '\u573a\u666f\u4fe1\u606f\u8868',
                'verbose_name_plural': '\u573a\u666f\u4fe1\u606f\u8868',
            },
        ),
        migrations.CreateModel(
            name='StaffInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bk_username', models.CharField(max_length=64, verbose_name='\u804c\u5458\u7528\u6237\u540d')),
                ('staff_position_id', models.IntegerField(verbose_name='\u804c\u5458\u5c97\u4f4dID')),
            ],
            options={
                'verbose_name': '\u804c\u5458\u4fe1\u606f\u8868',
                'verbose_name_plural': '\u804c\u5458\u4fe1\u606f\u8868',
            },
        ),
        migrations.CreateModel(
            name='StaffPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('staff_position_id', models.IntegerField(verbose_name='\u804c\u5458\u5c97\u4f4dID')),
                ('staff_position_name', models.CharField(max_length=64, verbose_name='\u5c97\u4f4d\u540d\u79f0')),
            ],
            options={
                'verbose_name': '\u5458\u5de5\u5c97\u4f4d\u8868',
                'verbose_name_plural': '\u5458\u5de5\u5c97\u4f4d\u8868',
            },
        ),
        migrations.CreateModel(
            name='StaffScene',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('staff_scene_id', models.IntegerField(verbose_name='\u7528\u6237\u573a\u666fID')),
                ('staff_scene_order_id', models.IntegerField(verbose_name='\u7528\u6237\u573a\u666f\u6392\u5e8fID')),
                ('bk_username', models.CharField(max_length=64, verbose_name='\u804c\u5458\u7528\u6237\u540d')),
                ('staff_scene_default_time', models.CharField(max_length=64, verbose_name='\u573a\u666f\u505c\u7559\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u5458\u5de5\u81ea\u5b9a\u4e49\u8bbe\u7f6e\u573a\u666f\u4fe1\u606f\u8868',
                'verbose_name_plural': '\u5458\u5de5\u81ea\u5b9a\u4e49\u8bbe\u7f6e\u573a\u666f\u4fe1\u606f\u8868',
            },
        ),
    ]
