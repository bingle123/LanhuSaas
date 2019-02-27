# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20190225_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.IntegerField(verbose_name='\u4f5c\u4e1a\u72b6\u6001'),
        ),
    ]
