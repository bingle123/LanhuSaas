# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bk_biz_id', models.CharField(max_length=16, verbose_name='\u4e1a\u52a1')),
                ('bk_cloud_id', models.CharField(max_length=16, verbose_name='\u4e91\u533a\u57df')),
                ('bk_os_type', models.CharField(default=b'Linux', max_length=64, verbose_name='\u7cfb\u7edf\u7c7b\u578b')),
                ('module_name', models.CharField(default=b'', max_length=64, verbose_name='\u6240\u5c5e\u6a21\u5757', blank=True)),
                ('inner_ip', models.GenericIPAddressField(verbose_name='\u5185\u7f51IP')),
                ('run_time', models.DateTimeField(auto_now_add=True, verbose_name='\u6267\u884c\u65f6\u95f4')),
                ('success', models.BooleanField(default=False, verbose_name='\u6267\u884c\u662f\u5426\u6210\u529f')),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u4fe1\u606f',
                'verbose_name_plural': '\u4e3b\u673a\u4fe1\u606f',
            },
        ),
    ]
