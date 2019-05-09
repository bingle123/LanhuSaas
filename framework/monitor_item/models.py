# -*- coding: utf-8 -*-

from django.db import models
from monitor_scene.models import Scene


class Monitor(models.Model):
    """
    单元信息表
    """
    monitor_name = models.CharField(verbose_name=u'监控项名称', max_length=50)
    monitor_type = models.PositiveIntegerField(verbose_name=u'监控项类型')
    jion_id = models.PositiveIntegerField(verbose_name=u'关联ID', null=True)
    gather_rule = models.CharField(verbose_name=u'采集规则', max_length=500)
    gather_params = models.CharField(verbose_name=u'采集参数', max_length=500)
    params = models.CharField(verbose_name=u'监控参数', max_length=500)
    width = models.PositiveIntegerField(verbose_name=u'宽')
    height = models.PositiveIntegerField(verbose_name=u'高')
    font_size = models.PositiveIntegerField(verbose_name=u'字体大小')
    period = models.PositiveIntegerField(verbose_name=u'采集周期')
    start_time = models.TimeField(verbose_name=u'开始时间')
    end_time = models.TimeField(verbose_name=u'结束时间')
    create_time = models.TimeField(verbose_name=u'创建时间', auto_now_add=True)
    creator = models.CharField(verbose_name=u'创建人', max_length=10)
    editor = models.CharField(verbose_name=u'编辑人', max_length=10)
    edit_time = models.DateTimeField(verbose_name=u'修改时间', auto_now=True)
    status = models.PositiveIntegerField(verbose_name=u'监控状态')
    contents = models.CharField(verbose_name=u'显示内容', max_length=500)
    monitor_area = models.IntegerField(verbose_name=u'监控项日历地区')
    source_type = models.PositiveIntegerField(verbose_name=u'来源类型', null=True)
    target_name = models.CharField(verbose_name=u'指标名称', max_length=40, null=True)
    measure_name = models.CharField(verbose_name=u'度量名称', max_length=50, null=True)
    dimension = models.CharField(verbose_name=u'维度', max_length=1000, null=True)
    display_type = models.PositiveIntegerField(verbose_name=u'展示类型', null=True)
    display_rule = models.CharField(verbose_name=u'展示规则', max_length=1000, null=True)
    score = models.PositiveIntegerField(verbose_name=u'分值', max_length=3, null=True)
    class Meta:
        verbose_name = u'监控项信息表'
        verbose_name_plural = u'监控项信息'
        db_table = 'tb_monitor_item'


class Job(models.Model):
    job_id = models.PositiveIntegerField(verbose_name=u'关联ID')
    instance_id = models.PositiveIntegerField(verbose_name=u'作业实列ID')
    status = models.IntegerField(verbose_name=u'作业状态')
    test_flag = models.PositiveIntegerField(verbose_name=u'测试标识')
    start_time = models.TimeField(verbose_name=u'开始时间', auto_now_add=True)
    job_log = models.CharField(verbose_name=u'作业日志', max_length=5000)

    class Meta:
        verbose_name = u'作业实列表'
        verbose_name_plural = u'作业实列信息'
        db_table = 'td_job_instance'


# status：0表示FAILED  1表示RUNNING   2表示SUSPEN DED   3表示REVOKED   4表示FINISHED 5表示超时
# test_flag 1表示测试  2表示非测试
class Flow(models.Model):
    flow_id = models.PositiveIntegerField(verbose_name=u'关联ID')
    instance_id = models.PositiveIntegerField(verbose_name=u'流程实列ID')
    status = models.PositiveIntegerField(verbose_name=u'节点状态')
    test_flag = models.PositiveIntegerField(verbose_name=u'测试标识')
    start_time = models.TimeField(verbose_name=u'开始时间', auto_now_add=True)

    class Meta:
        verbose_name = u'流程实列表'
        verbose_name_plural = u'流程实列信息'
        db_table = 'td_flow_instance'


class Flow_Node(models.Model):
    flow_id = models.PositiveIntegerField(verbose_name=u'流程ID')
    node_name = models.CharField(verbose_name=u'节点名称', max_length=50)
    start_time = models.CharField(verbose_name=u'开始时间', max_length=50)
    end_time = models.CharField(verbose_name=u'结束时间', max_length=50)

    class Meta:
        verbose_name = u'流程节点表'
        verbose_name_plural = u'流程节点信息'
        db_table = 'tb_flow_node'


class Scene_monitor(models.Model):
    scene_id = models.PositiveIntegerField(verbose_name=u'场景ID')
    item_id = models.PositiveIntegerField(verbose_name=u'监控项ID')
    x = models.PositiveIntegerField(verbose_name=u'x坐标')
    y = models.PositiveIntegerField(verbose_name=u'y坐标')
    scale = models.DecimalField(verbose_name=u'比例', max_digits=4, decimal_places=2)
    score = models.PositiveIntegerField(verbose_name=u'打分')
    order = models.PositiveIntegerField(verbose_name=u'排序')
    next_item = models.PositiveIntegerField(verbose_name=u'下一个监控项')

    class Meta:
        verbose_name = u'场景监控项'
        verbose_name_plural = u'场景监控项'
        db_table = "tl_scene_monitor"


class Scene_node(models.Model):
    pos_id = models.PositiveIntegerField(verbose_name=u'场景ID')
    item_id = models.PositiveIntegerField(verbose_name=u'监控项ID')
    node_id = models.PositiveIntegerField(verbose_name=u'节点ID')
    score = models.PositiveIntegerField(verbose_name=u'打分')

    class Meta:
        verbose_name = u'节点打分表'
        verbose_name_plural = u'节点打分'
        db_table = "td_scene_node"
