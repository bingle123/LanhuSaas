# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobManagement', '0005_auto_20190124_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localuser',
            name='job_id',
            field=models.IntegerField(verbose_name='\u7528\u6237\u6240\u5c5e\u5c97\u4f4d'),
        ),
    ]
