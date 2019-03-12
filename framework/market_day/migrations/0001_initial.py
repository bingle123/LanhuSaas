# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', models.CharField(max_length=30, verbose_name='\u56fd\u5bb6')),
                ('timezone', models.CharField(max_length=30, verbose_name='\u65f6\u533a')),
            ],
            options={
                'db_table': 'area',
            },
        ),
        migrations.CreateModel(
            name='HeaderData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('header', models.TextField()),
                ('edit_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'db_table': 'header_data',
            },
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.CharField(max_length=30)),
                ('flag', models.IntegerField(null=True)),
                ('area', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'holiday',
            },
        ),
    ]
