# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('position', '0002_auto_20190124_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='localuser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=50, verbose_name='\u7528\u6237\u540d\u79f0')),
                ('job_id', models.IntegerField(max_length=11, verbose_name='\u7528\u6237\u6240\u5c5e\u5c97\u4f4d')),
                ('user_tel', models.CharField(max_length=20, verbose_name='\u7528\u6237\u624b\u673a')),
                ('user_email', models.CharField(max_length=50, verbose_name='\u7528\u6237\u90ae\u7bb1')),
                ('wechat_openid', models.CharField(max_length=50, verbose_name='\u7528\u6237\u540d\u79f0')),
                ('infrom', models.IntegerField(max_length=1, verbose_name='\u901a\u77e5\u65b9\u5f0f')),
                ('alarm', models.IntegerField(max_length=1, verbose_name='\u544a\u8b66\u65b9\u5f0f')),
            ],
            options={
                'db_table': 'tb_local_user',
                'verbose_name': '\u7528\u6237\u4fe1\u606f\u8868',
            },
        ),
    ]
