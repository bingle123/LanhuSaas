# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operatelog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_type', models.CharField(max_length=100, verbose_name='\u64cd\u4f5c\u7c7b\u578b')),
                ('log_name', models.CharField(max_length=100, verbose_name='\u65e5\u5fd7\u540d\u79f0')),
                ('user_name', models.CharField(max_length=100, verbose_name='\u7528\u6237\u540d\u79f0')),
                ('class_name', models.CharField(max_length=100, verbose_name='\u7c7b\u540d\u79f0')),
                ('method', models.CharField(max_length=500, verbose_name='\u65b9\u6cd5\u540d\u79f0')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('succeed', models.CharField(max_length=50, verbose_name='\u662f\u5426\u6210\u529f')),
                ('message', models.CharField(max_length=500, verbose_name='\u5907\u6ce8')),
            ],
            options={
                'db_table': 'td_operate_log',
                'verbose_name': '\u64cd\u4f5c\u65e5\u5fd7\u8bb0\u5f55',
            },
        ),
    ]
