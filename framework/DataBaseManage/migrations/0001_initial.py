# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('connname', models.CharField(max_length=30, verbose_name='\u8fde\u63a5\u540d\u79f0')),
                ('type', models.CharField(max_length=30, verbose_name='\u8fde\u63a5\u7c7b\u578b')),
                ('ip', models.CharField(max_length=30, verbose_name='ip\u5730\u5740')),
                ('port', models.CharField(max_length=50, verbose_name='\u7aef\u53e3')),
                ('username', models.CharField(max_length=155, verbose_name='\u7528\u6237\u540d')),
                ('databasename', models.CharField(max_length=125, verbose_name='\u6570\u636e\u5e93\u540d\u79f0')),
                ('password', models.CharField(max_length=155, verbose_name='\u5bc6\u7801')),
            ],
        ),
    ]
