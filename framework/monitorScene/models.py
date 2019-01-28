# -*- coding: utf-8 -*-
from django.db import models
from jobManagement.models import JobInstance
from monitor.models import Monitor


class Scene(models.Model):
    """
    场景信息表
    """
    scene_name = models.CharField(verbose_name=u'场景名称', max_length=50)
    scene_startTime = models.TimeField(verbose_name=u'开始时间')
    scene_endTime = models.TimeField(verbose_name=u'结束时间')
    scene_creator = models.CharField(verbose_name=u'创建人', max_length=50)
    scene_creator_time = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    scene_editor = models.CharField(verbose_name=u'编辑人', max_length=50)
    scene_editor_time = models.DateTimeField(verbose_name=u'编辑时间', auto_now=True)
    class Meta:
        verbose_name = u'场景信息'
        verbose_name_plural = u'场景信息'
        db_table = "tb_monitor_scene"

class position_scene(models.Model):
    position_id = models.PositiveIntegerField(verbose_name=u'岗位id')
    scene = models.ForeignKey(related_name='scene_id',to='Scene', to_field='id', on_delete=models.CASCADE)
    class Meta:
        verbose_name = u'岗位与场景关系表'
        verbose_name_plural = u'岗位与场景关系表'
        db_table = "tl_position_scene"
