# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataBaseManage', '0002_tdatabase'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TDataBase',
        ),
    ]
