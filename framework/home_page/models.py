# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class WorkTime(models.Model):
    name = models.CharField(max_length=256, verbose_name=u"名称", null=True)
    startTime = models.TimeField(verbose_name=u"开始时间", null=True)
    endTime = models.TimeField(verbose_name=u"开始时间", null=True)

    class Meta:
        db_table = 'kt_home_page'
