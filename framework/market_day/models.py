# -*- coding: utf-8 -*-

from django.db import models


class Holiday(models.Model):
    day=models.CharField(max_length=30)
    flag=models.IntegerField(null=True)
    area=models.IntegerField(null=True)
    def __unicode__(self):
        return self.day
    class Meta:
        db_table='holiday'

class HeaderData(models.Model):
    header=models.TextField()
    edit_time=models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    def __unicode__(self):
        return self.day
    class Meta:
        db_table='header_data'