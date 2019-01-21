# -*- coding: utf-8 -*-
from django.db import models

class Scene(models.Model):
    """
    场景信息表
    """
    scene_name = models.CharField(verbose_name=u'场景名称', max_length=20)
    scene_startTime = models.DateTimeField(verbose_name=u'开始时间')
    scene_endTime = models.DateTimeField(verbose_name=u'结束时间')
    scene_positions = models.CharField(verbose_name=u'岗位', max_length=20)
    scene_creator = models.CharField(verbose_name=u'创建人', max_length=20)
    scene_creator_time = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    scene_editor = models.CharField(verbose_name=u'编辑人', max_length=24)
    scene_editor_time = models.DateTimeField(verbose_name=u'编辑时间', auto_now=True)


    class Meta:
        verbose_name = u'场景信息'
        verbose_name_plural = u'场景信息'
        db_table = "monitor_scene"