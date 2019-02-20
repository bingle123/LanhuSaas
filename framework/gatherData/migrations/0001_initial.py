# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TDGatherData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_id', models.PositiveIntegerField(verbose_name='\u76d1\u63a7\u9879ID')),
                ('instance_id', models.PositiveIntegerField(null=True, verbose_name='\u76d1\u63a7\u5b9e\u4f8bID')),
                ('gather_time', models.DateTimeField(null=True, verbose_name='\u91c7\u96c6\u65f6\u95f4')),
                ('data_key', models.CharField(max_length=50, null=True, verbose_name='\u6570\u636eKEY')),
                ('data_value', models.CharField(max_length=500, null=True, verbose_name='\u6570\u636eVALUE')),
                ('gather_error_log', models.CharField(max_length=5000, verbose_name='\u91c7\u96c6\u9519\u8bef\u65e5\u5fd7')),
            ],
            options={
                'db_table': 'td_gather_data',
            },
        ),
    ]
