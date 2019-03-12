# -*- coding: utf-8 -*-
from django.db import models

class operation_report(models.Model):
    """
         运行情况报表
    """
    date = models.CharField(verbose_name=u'日期', max_length=10,)
    scene_num = models.CharField(verbose_name=u'运行场景数',max_length=10)
    success_num = models.CharField(verbose_name=u'成功数', max_length=10,)
    success_rate = models.CharField(verbose_name=u'成功率',max_length=10,)
    failed_num = models.CharField(verbose_name=u'失败数', max_length=50,)
    alert_num = models.CharField(verbose_name=u'告警数', max_length=10, )
    class Meta:
        verbose_name = u'运行情况报表'
        db_table = 'td_operation_report'