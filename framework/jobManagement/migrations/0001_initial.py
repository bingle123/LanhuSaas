# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_name', models.CharField(max_length=50, verbose_name='\u5c97\u4f4d\u540d\u79f0')),
                ('create_Time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('edit_time', models.DateTimeField(auto_now_add=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('create_person', models.CharField(max_length=50, verbose_name='\u4fee\u6539\u4eba')),
            ],
            options={
                'db_table': 'tb_job_basic_info',
                'verbose_name': '\u5c97\u4f4d\u4fe1\u606f\u8868',
                'verbose_name_plural': '\u5355\u5143\u4fe1\u606f',
            },
        ),
    ]
