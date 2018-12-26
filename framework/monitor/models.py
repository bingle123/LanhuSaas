# -*- coding: utf-8 -*-
from django.db import models

class unit_administration(models.Model):
    """
    单元信息表
    """
    unit_name = models.CharField(verbose_name=u'单元名称', max_length=200, unique=True)
    unit_type = models.CharField(verbose_name=u'单元类型', max_length=200)
    editor = models.CharField(verbose_name=u'编辑人', max_length=200)
    edit_time = models.CharField(verbose_name=u'修改时间', max_length=200)
    font_size = models.PositiveIntegerField(verbose_name=u'字号')
    hight = models.PositiveIntegerField(verbose_name=u'高')
    wide = models.PositiveIntegerField(verbose_name=u'宽')
    content = models.CharField(verbose_name=u'显示内容', max_length=2000)
    data_source = models.CharField(verbose_name=u'数据来源', max_length=200)
    time_slot = models.CharField(verbose_name=u'时间段', max_length=200)
    time_interval = models.PositiveIntegerField(verbose_name=u'间隔时间秒')
    template = models.CharField(verbose_name=u'数据库和模板', max_length=200)
    chart_type = models.CharField(verbose_name=u'图表类型', max_length=200)
    parameter = models.CharField(verbose_name=u'文件内容、脚本参数、模板参数', max_length=5000)


    class Meta:
        verbose_name = u'单元信息'
        verbose_name_plural = u'单元信息'