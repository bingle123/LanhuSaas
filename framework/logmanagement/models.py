# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Operatelog(models.Model):
    """
        操作日志记录
    """
    log_type = models.CharField(verbose_name=u'操作类型', max_length=100)
    log_name = models.CharField(verbose_name=u'日志名称', max_length=100)
    user_name = models.CharField(verbose_name=u'用户名称', max_length=100)
    class_name = models.CharField(verbose_name=u'类名称', max_length=100)
    method = models.CharField(verbose_name=u'方法名称', max_length=500)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    succeed = models.CharField(verbose_name=u'是否成功', max_length=50)
    message = models.CharField(verbose_name=u'备注', max_length=500)
    class Meta:
        verbose_name = u'操作日志记录'
        db_table = 'td_operate_log'
