# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scene_monitor',
            name='scale',
            field=models.DecimalField(verbose_name='\u6bd4\u4f8b', max_digits=4, decimal_places=2),
        ),
    ]
