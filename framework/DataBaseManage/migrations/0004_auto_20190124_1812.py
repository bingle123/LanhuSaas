# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('DataBaseManage', '0003_delete_tdatabase'),
    ]

    operations = [
        migrations.AddField(
            model_name='conn',
            name='createname',
            field=models.CharField(default=datetime.datetime(2019, 1, 24, 18, 12, 41, 387000), max_length=64, verbose_name='\u521b\u5efa\u4eba'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conn',
            name='createtime',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 24, 18, 12, 44, 632000), verbose_name='\u521b\u5efa\u65f6\u95f4', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conn',
            name='editname',
            field=models.CharField(default=datetime.datetime(2019, 1, 24, 18, 12, 46, 805000), max_length=64, verbose_name='\u4fee\u6539\u4eba'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conn',
            name='edittime',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 24, 18, 12, 48, 450000), verbose_name='\u4fee\u6539\u65f6\u95f4', auto_now=True),
            preserve_default=False,
        ),
    ]
