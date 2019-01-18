# -*- coding: utf-8 -*-
from django.db import models


class Common(models.Model):
    """
    单元信息表
    """
    unit_name = models.CharField(verbose_name=u'单元名称', max_length=40, unique=True)
    unit_type = models.CharField(verbose_name=u'单元类型', max_length=20)
    editor = models.CharField(verbose_name=u'编辑人', max_length=20)
    edit_time = models.DateTimeField(verbose_name=u'修改时间', auto_now=True)
    font_size = models.PositiveIntegerField(verbose_name=u'字号')
    height = models.PositiveIntegerField(verbose_name=u'高')
    wide = models.PositiveIntegerField(verbose_name=u'宽')
    switch = models.CharField(verbose_name=u'开关', max_length=10)
    start_time = models.TimeField(verbose_name=u'开始时间')
    end_time = models.TimeField(verbose_name=u'结束时间')
    cycle = models.PositiveIntegerField(verbose_name=u'采集周期')


class BasicUnit(models.Model):
    """
    基本单元表
    """
    unit_id = models.PositiveIntegerField(verbose_name=u'单元id', primary_key=True)
    contents = models.CharField(verbose_name=u'显示内容', max_length=100)
    sql_file_interface = models.CharField(verbose_name=u'数据来源', max_length=20)
    sql = models.CharField(verbose_name=u'连接数据库', max_length=20)
    rules = models.CharField(verbose_name=u'采集规则', max_length=100)
    server = models.CharField(verbose_name=u'服务器', max_length=20)
    file = models.CharField(verbose_name=u'文件路径', max_length=50)
    urls = models.CharField(verbose_name=u'接口url', max_length=100)
    param = models.CharField(verbose_name=u'接口参数', max_length=20)


class ChartUnit(models.Model):
    """
    图表单元
    """
    unit_id = models.PositiveIntegerField(verbose_name=u'单元id', primary_key=True)
    contents = models.CharField(verbose_name=u'显示内容', max_length=100)
    chart_type = models.CharField(verbose_name=u'图表类型', max_length=20)
    sql = models.CharField(verbose_name=u'连接数据库', max_length=20)
    rules = models.CharField(verbose_name=u'采集规则', max_length=100)


class JobUnit(models.Model):
    unit_id = models.PositiveIntegerField(verbose_name=u'单元id', primary_key=True)
    contents = models.CharField(verbose_name=u'显示内容', max_length=100)
    job_mould = models.CharField(verbose_name=u'作业模板', max_length=50)
    NODE_KEY = models.CharField(verbose_name=u'NODE_KEY', max_length=50)
    server = models.CharField(verbose_name=u'执行服务器', max_length=20)


class FlowUnit(models.Model):
    unit_id = models.PositiveIntegerField(verbose_name=u'单元id', primary_key=True)
    flow_mould = models.CharField(verbose_name=u'流程模板', max_length=50)
    param = models.CharField(verbose_name=u'模板参数', max_length=20)
    node = models.CharField(verbose_name=u'节点名称', max_length=20)
