# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class JobInstance(models.Model):
    """
        岗位信息表
    """
    Job_name = models.CharField(verbose_name=u'岗位名称', max_length=20,)
    User_name = models.CharField(verbose_name=u'员工姓名', max_length=20)
    Start_Time = models.DateField(verbose_name=u'创建时间',auto_now = True)
    Status = models.CharField(verbose_name=u'状态', max_length=20)
    log = models.CharField(verbose_name=u'日志', max_length=50)

class Meta:
    verbose_name = u'岗位信息表'
    verbose_name_plural = u'单元信息'