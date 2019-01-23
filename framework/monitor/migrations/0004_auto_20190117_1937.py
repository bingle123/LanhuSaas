# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_common_switch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='common',
            name='end_time',
            field=models.TimeField(verbose_name='\u7ed3\u675f\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='common',
            name='start_time',
            field=models.TimeField(verbose_name='\u5f00\u59cb\u65f6\u95f4'),
        ),
    ]
