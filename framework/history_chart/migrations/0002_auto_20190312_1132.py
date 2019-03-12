# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history_chart', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='operation_report',
            table='td_operation_report',
        ),
    ]
