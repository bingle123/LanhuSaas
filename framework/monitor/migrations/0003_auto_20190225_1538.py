# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20190224_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitor',
            name='monitor_name',
            field=models.CharField(max_length=50, verbose_name='\u76d1\u63a7\u9879\u540d\u79f0'),
        ),
    ]
