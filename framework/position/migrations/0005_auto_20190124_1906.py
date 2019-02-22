# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('position', '0004_auto_20190124_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localuser',
            name='alarm',
            field=models.IntegerField(verbose_name='\u544a\u8b66\u65b9\u5f0f'),
        ),
        migrations.AlterField(
            model_name='localuser',
            name='infrom',
            field=models.IntegerField(verbose_name='\u901a\u77e5\u65b9\u5f0f'),
        ),
    ]
