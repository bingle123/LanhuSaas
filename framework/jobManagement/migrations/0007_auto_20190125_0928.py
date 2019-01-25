# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobManagement', '0006_auto_20190124_1906'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobinstance',
            old_name='create_person',
            new_name='creator',
        ),
        migrations.RenameField(
            model_name='jobinstance',
            old_name='edit_person',
            new_name='editor',
        ),
        migrations.RenameField(
            model_name='jobinstance',
            old_name='job_name',
            new_name='pos_name',
        ),
        migrations.RenameField(
            model_name='localuser',
            old_name='alarm',
            new_name='alert_style',
        ),
        migrations.RenameField(
            model_name='localuser',
            old_name='user_email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='localuser',
            old_name='user_tel',
            new_name='mobile_no',
        ),
        migrations.RenameField(
            model_name='localuser',
            old_name='infrom',
            new_name='notice_style',
        ),
        migrations.RenameField(
            model_name='localuser',
            old_name='wechat_openid',
            new_name='open_id',
        ),
        migrations.RenameField(
            model_name='localuser',
            old_name='job_id',
            new_name='user_pos',
        ),
        migrations.AlterModelTable(
            name='jobinstance',
            table='tb_pos_info',
        ),
        migrations.AlterModelTable(
            name='localuser',
            table='tb_user_info',
        ),
    ]
