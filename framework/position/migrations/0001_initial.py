# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='pos_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pos_name', models.CharField(max_length=50, verbose_name='\u5c97\u4f4d\u540d\u79f0')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('creator', models.CharField(max_length=50, verbose_name='\u521b\u5efa\u4eba')),
                ('edit_time', models.DateTimeField(auto_now_add=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('editor', models.CharField(max_length=50, verbose_name='\u4fee\u6539\u4eba')),
            ],
            options={
                'db_table': 'tb_pos_info',
                'verbose_name': '\u5c97\u4f4d\u4fe1\u606f\u8868',
                'verbose_name_plural': '\u5355\u5143\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='user_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=50, verbose_name='\u7528\u6237\u540d\u79f0')),
                ('mobile_no', models.CharField(max_length=20, verbose_name='\u7528\u6237\u624b\u673a')),
                ('email', models.CharField(max_length=50, verbose_name='\u7528\u6237\u90ae\u7bb1')),
                ('open_id', models.CharField(max_length=50, verbose_name='\u5fae\u4fe1openid')),
                ('notice_style', models.CharField(max_length=10, verbose_name='\u901a\u77e5\u65b9\u5f0f')),
                ('alert_style', models.CharField(max_length=10, verbose_name='\u544a\u8b66\u65b9\u5f0f')),
                ('user_pos', models.ForeignKey(to='position.pos_info', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'db_table': 'tb_user_info',
                'verbose_name': '\u7528\u6237\u4fe1\u606f\u8868',
            },
        ),
    ]
