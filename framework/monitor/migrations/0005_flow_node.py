# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0004_auto_20190221_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='flow_node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flow_id', models.PositiveIntegerField(verbose_name='\u6d41\u7a0bID')),
                ('node_name', models.CharField(max_length=50, verbose_name='\u8282\u70b9\u540d\u79f0')),
                ('start_time', models.TimeField(verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('end_time', models.TimeField(verbose_name='\u7ed3\u675f\u65f6\u95f4')),
            ],
            options={
                'db_table': 'tb_flow_node',
                'verbose_name': '\u6d41\u7a0b\u8282\u70b9\u8868',
                'verbose_name_plural': '\u6d41\u7a0b\u8282\u70b9\u4fe1\u606f',
            },
        ),
    ]
