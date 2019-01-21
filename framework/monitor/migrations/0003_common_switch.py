# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20190117_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='common',
            name='switch',
            field=models.CharField(default=1, max_length=10, verbose_name='\u5f00\u5173'),
            preserve_default=False,
        ),
    ]
