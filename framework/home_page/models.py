# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class WorkTime(models.Model):
    name = models.CharField(max_length=256, verbose_name=u"名称", null=True)
    startTime = models.TimeField(verbose_name=u"开始时间", null=True)
    endTime = models.TimeField(verbose_name=u"开始时间", null=True)

    class Meta:
        db_table = 'kt_home_page'



class AlertInfo(models.Model):
    alert_txt = models.CharField(max_length=200, verbose_name=u"警告内容", blank=True, null=True)
    alert_time = models.DateTimeField(blank=True, verbose_name=u"警告时间", null=True)
    alert_level_code = models.SmallIntegerField(verbose_name=u"警告级别代码", blank=True, null=True)
    alert_level_name = models.CharField(max_length=50, verbose_name=u"警告级别名称",  blank=True, null=True)
    alert_status_code = models.CharField(max_length=10, verbose_name=u"状态代码",  blank=True, null=True)
    alert_status_name = models.CharField(max_length=50, verbose_name=u"状态名称",  blank=True, null=True)
    modify_time = models.DateTimeField(verbose_name=u"最后一次修改时间", blank=True, null=True)
    scene_id = models.IntegerField(verbose_name=u"场景id", blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'td_alert_info'