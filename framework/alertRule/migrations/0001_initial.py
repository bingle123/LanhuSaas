# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TdAlertLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rule_id', models.IntegerField(null=True, verbose_name='\u544a\u8b66\u89c4\u5219id')),
                ('item_id', models.PositiveIntegerField(verbose_name='\u76d1\u63a7\u9879ID')),
                ('alert_title', models.CharField(max_length=100, verbose_name='\u544a\u8b66\u6807\u9898')),
                ('alert_content', models.CharField(max_length=2000, verbose_name='\u544a\u8b66\u5185\u5bb9')),
                ('alert_time', models.DateTimeField(auto_now_add=True, verbose_name='\u544a\u8b66\u65f6\u95f4')),
                ('persons', models.CharField(max_length=1000, verbose_name='\u7ed9\u8c01\u53d1\u7684')),
            ],
            options={
                'db_table': 'td_alert_log',
            },
        ),
    ]
