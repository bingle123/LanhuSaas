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
                ('upper_limit', models.DecimalField(verbose_name='\u4e0a\u9650\u503c', max_digits=10, decimal_places=4)),
                ('lower_limit', models.DecimalField(verbose_name='\u4e0b\u9650\u503c', max_digits=10, decimal_places=4)),
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
    ]
