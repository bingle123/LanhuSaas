# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20190128_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flow',
            name='flow_id',
            field=models.PositiveIntegerField(verbose_name='\u5173\u8054ID'),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_id',
            field=models.PositiveIntegerField(verbose_name='\u5173\u8054ID'),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='jion_id',
            field=models.PositiveIntegerField(verbose_name='\u5173\u8054ID'),
        ),
    ]
