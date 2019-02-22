# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('position', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobinstance',
            old_name='create_Time',
            new_name='create_time',
        ),
    ]
