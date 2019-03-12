# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operation_report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.CharField(max_length=10, verbose_name='\u65e5\u671f')),
                ('scene_num', models.CharField(max_length=10, verbose_name='\u8fd0\u884c\u573a\u666f\u6570')),
                ('success_num', models.CharField(max_length=10, verbose_name='\u6210\u529f\u6570')),
                ('success_rate', models.CharField(max_length=10, verbose_name='\u6210\u529f\u7387')),
                ('failed_num', models.CharField(max_length=50, verbose_name='\u5931\u8d25\u6570')),
                ('alert_num', models.CharField(max_length=10, verbose_name='\u544a\u8b66\u6570')),
            ],
            options={
                'db_table': 'td_Operation_report',
                'verbose_name': '\u8fd0\u884c\u60c5\u51b5\u62a5\u8868',
            },
        ),
    ]
