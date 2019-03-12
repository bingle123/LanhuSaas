# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TbAlertRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_id', models.PositiveIntegerField(verbose_name='\u76d1\u63a7\u9879ID')),
                ('key_name', models.CharField(max_length=50, verbose_name='\u6570\u636ekey\u540d\u79f0')),
                ('rule_name', models.CharField(max_length=50, verbose_name='\u89c4\u5219\u540d\u79f0')),
                ('upper_limit', models.DecimalField(null=True, verbose_name='\u4e0a\u9650\u503c', max_digits=10, decimal_places=4)),
                ('lower_limit', models.DecimalField(null=True, verbose_name='\u4e0b\u9650\u503c', max_digits=10, decimal_places=4)),
                ('alert_title', models.CharField(max_length=100, verbose_name='\u544a\u8b66\u6807\u9898')),
                ('alert_content', models.CharField(max_length=2000, verbose_name='\u544a\u8b66\u5185\u5bb9')),
                ('create_time', models.DateTimeField(verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('creator', models.CharField(max_length=50, verbose_name='\u521b\u5efa\u4eba')),
                ('edit_time', models.DateTimeField(verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('editor', models.CharField(max_length=50, verbose_name='\u4fee\u6539\u4eba')),
            ],
            options={
                'db_table': 'tb_alert_rule',
            },
        ),
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
        migrations.CreateModel(
            name='TlAlertUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rule_id', models.IntegerField(verbose_name='\u89c4\u5219\u5916\u952e')),
                ('user_id', models.IntegerField(verbose_name='\u7528\u6237\u5916\u952e')),
            ],
            options={
                'db_table': 'tl_alert_user',
            },
        ),
    ]
