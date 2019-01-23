# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lcz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TDataBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='\u6570\u636e\u5e93\u540d\u79f0')),
            ],
        ),
    ]
