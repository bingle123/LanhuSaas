# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class JobInstance(models.Model):
    """
        岗位信息表
    """
    job_name = models.CharField(verbose_name=u'岗位名称', max_length=50,)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    create_person = models.CharField(verbose_name=u'创建人', max_length=50,)
    edit_time = models.DateTimeField(verbose_name=u'修改时间', auto_now_add=True)
    edit_person = models.CharField(verbose_name=u'修改人', max_length=50, )

    class Meta:
        verbose_name = u'岗位信息表'
        verbose_name_plural = u'单元信息'
        db_table = 'tb_job_basic_info'