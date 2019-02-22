# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('position', '0003_localuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localuser',
            name='wechat_openid',
            field=models.CharField(max_length=50, verbose_name='\u5fae\u4fe1openid'),
        ),
    ]
