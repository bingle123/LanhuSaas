# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='holiday',
            fields=[
                ('day', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('year', models.CharField(max_length=10)),
            ],
        ),
    ]
