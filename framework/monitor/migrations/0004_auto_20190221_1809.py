# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20190215_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flow',
            name='instance_id',
            field=models.PositiveIntegerField(verbose_name='\u6d41\u7a0b\u5b9e\u5217ID'),
        ),
        migrations.AlterField(
            model_name='flow',
            name='start_time',
            field=models.TimeField(auto_now_add=True, verbose_name='\u5f00\u59cb\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_log',
            field=models.CharField(max_length=5000, verbose_name='\u4f5c\u4e1a\u65e5\u5fd7'),
        ),
        migrations.AlterField(
            model_name='job',
            name='start_time',
            field=models.TimeField(auto_now_add=True, verbose_name='\u5f00\u59cb\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='gather_rule',
            field=models.CharField(max_length=500, verbose_name='\u91c7\u96c6\u89c4\u5219'),
        ),
    ]
