# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('position', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pos_info',
            name='pos_name',
            field=models.CharField(unique=True, max_length=50, verbose_name='\u5c97\u4f4d\u540d\u79f0'),
        ),
    ]
