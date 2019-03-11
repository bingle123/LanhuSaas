# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class pos_info(models.Model):
    """
        岗位基本信息表
    """
    pos_name = models.CharField(verbose_name=u'岗位名称', max_length=50,)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    creator = models.CharField(verbose_name=u'创建人', max_length=50,)
    edit_time = models.DateTimeField(verbose_name=u'修改时间', auto_now_add=True)
    editor = models.CharField(verbose_name=u'修改人', max_length=50,)
    class Meta:
        verbose_name = u'岗位信息表'
        verbose_name_plural = u'单元信息'
        db_table = 'tb_pos_info'


class user_info(models.Model):
    """
        本地用户表
    """
    user_name = models.CharField(verbose_name=u'用户名称', max_length=50,)
    user_pos = models.ForeignKey('pos_info',on_delete=models.PROTECT)
    mobile_no = models.CharField(verbose_name=u'用户手机', max_length=20,)
    email = models.CharField(verbose_name=u'用户邮箱', max_length=50,)
    open_id = models.CharField(verbose_name=u'微信openid', max_length=50,)
    notice_style = models.CharField(verbose_name=u'通知方式', max_length=10)
    alert_style = models.CharField(verbose_name=u'告警方式',  max_length=10)
    class Meta:
        verbose_name = u'用户信息表'
        db_table = 'tb_user_info'