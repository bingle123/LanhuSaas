# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TbCustProcess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node_name', models.CharField(default=b'', max_length=50, verbose_name='\u8282\u70b9\u540d\u79f0')),
                ('send_content', models.CharField(default=b'', max_length=1000, verbose_name='\u901a\u77e5\u5185\u5bb9')),
                ('seq', models.PositiveIntegerField(verbose_name='\u987a\u5e8f')),
                ('receivers', models.CharField(default=b'', max_length=2000, verbose_name='\u901a\u77e5\u63a5\u6536\u4eba')),
            ],
            options={
                'db_table': 'tb_cust_process',
            },
        ),
        migrations.CreateModel(
            name='TdCustProcessLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_done', models.CharField(default=b'n', max_length=1, verbose_name='\u662f\u5426\u6267\u884c')),
                ('do_time', models.DateTimeField(null=True, verbose_name='\u6267\u884c\u65f6\u95f4')),
                ('do_person', models.CharField(max_length=50, null=True, verbose_name='\u6267\u884c\u4eba')),
                ('node', models.ForeignKey(verbose_name='\u8282\u70b9ID', to='customProcess.TbCustProcess')),
            ],
            options={
                'db_table': 'td_cust_process_log',
            },
        ),
    ]
