# -*- coding: utf-8 -*-
from django.db import models
import tools
# 临时
import json
import datetime
from django.core import serializers
# Create your models here.


class Host(models.Model):
    """主机信息"""
    bk_biz_name = models.CharField (u'业务', max_length=50)
    bk_cloud_name = models.CharField (u'云区域', max_length=200)
    bk_biz_id = models.CharField (u'业务', max_length=16)
    bk_cloud_id = models.CharField (u'云区域', max_length=16)
    bk_os_type = models.CharField (u'系统类型', max_length=64, default='Linux')
    module_name = models.CharField (u'所属模块', max_length=64, blank=True, default='')
    inner_ip = models.GenericIPAddressField (u'内网IP')
    run_time = models.DateTimeField (u'执行时间', auto_now_add=True)
    success = models.BooleanField(u'执行是否成功',default=False)

    def __unicode__(self):
        return '{}.{}.{}'.format(self.inner_ip,
                                 self.bk_biz_id,
                                 self.bk_cloud_id)

    class Meta:
        verbose_name = u'主机信息'
        verbose_name_plural = u'主机信息'


class StaffInfoManage(models.Manager):
    """
    用户信息管理
    """
    def get_staff_info(self, bk_username):
        try:
            res = StaffInfo.objects.get(bk_username=bk_username)
            # res.toDic()
            dict = res.__dict__
            del dict['_state']
            result = {"code": True, "result": dict, "message": u"查询成功" }
        except Exception, e:
            result = {"code": False, "result": None, "message": u"查询失败 %s" % e}
        return result

    def save_staff_info(self, data):
        try:
            StaffInfo.objects.create(
                staff_position_id=data.get("staff_position_id"),
                bk_username=data.get("bk_username")
            )
            result = {"code": True, "message": u"保存成功"}
        except Exception, e:
            result = {"code": False, "message": u"保存失败 %s" % e}
        return result


class StaffInfo(models.Model):
    """
    职员信息表
    """
    bk_username = models.CharField(u'职员用户名', max_length=64)
    staff_position_id = models.IntegerField(u'职员岗位ID')
    objects = StaffInfoManage()

    def toDic(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])

    def __unicode__(self):
        return self.bk_username

    class Meta:
        verbose_name = u'职员信息表'
        verbose_name_plural = u'职员信息表'


class SceneManage(models.Manager):
    """
    场景表管理
    """
    def get_scenes_all(self):
        try:
            res = Scene.objects.all().values()
            result_list = []
            for i in res:
                i['scene_start_time'] = i['scene_start_time'].strftime("%H:%M:%S")
                i['scene_stop_time'] = i['scene_stop_time'].strftime("%H:%M:%S")
                result_list.append(i)
            result = {"code": True, "result": result_list, "message": u"查询成功" }
        except Exception, e:
            result = {"code": False, "result": None, "message": u"查询失败" }
        return result

    def get_scene_by_staff_position_id(self, staff_position_id):
        """返回json数据"""
        try:
            res = Scene.objects.filter(staff_position_id=staff_position_id).values()
            temp_list = []
            for i in res:
                i['scene_start_time'] = i['scene_start_time'].strftime("%H:%M:%S")
                i['scene_stop_time'] = i['scene_stop_time'].strftime("%H:%M:%S")
                temp_list.append(i)
            result = {"code": True, "result": temp_list, "message": "根据场景ID查询成功"}
        except Exception, e:
            result = {"code": False, "result": None, "message": "根据场景ID查询失败 %s" % e}
        return result

    def get_scene_by_staff_position_id_time_order_by_scene_order_id(self, staff_position_id, now_time):
        """
        获取场景信息---顺序排序
        :param staff_position_id:   职位ID
        :param now_time:            时间
        :return:
        """
        try:
            res = Scene.objects.filter(staff_position_id=staff_position_id, scene_start_time__lt=now_time,
                                       scene_stop_time__gt=now_time).order_by('scene_order_id').values()
            temp_list = []
            for i in res:
                i['scene_start_time'] = i['scene_start_time'].strftime("%H:%M:%S")
                i['scene_stop_time'] = i['scene_stop_time'].strftime("%H:%M:%S")
                temp_list.append(i)
            result = {"code": True, "result": temp_list, "message": "根据场景ID查询成功"}
        except Exception, e:
            result = {"code": False, "result": None, "message": "根据场景ID查询失败 %s" % e}
        return result


class Scene(models.Model):
    """
    场景信息表
    """
    scene_id = models.IntegerField(u'场景ID')
    scene_name = models.CharField(u'场景名称', max_length=64)
    scene_example = models.CharField(u'场景实例', max_length=64)
    scene_start_time = models.TimeField(auto_now=True)
    scene_stop_time = models.TimeField(auto_now=True)
    scene_default_time = models.CharField(u'场景停留时间', max_length=64)
    scene_order_id = models.IntegerField(u'场景排序ID')
    staff_position_id = models.IntegerField(u'职员岗位ID')
    objects = SceneManage()

    def __unicode__(self):
        return "%d" % self.int

    class Meta:
        verbose_name = u'场景信息表'
        verbose_name_plural = u'场景信息表'


class StaffPositionManage(models.Manager):
    """
    用户岗位表管理
    """
    def get_positions_all(self):
        """
        获取所有岗位信息
        :return:
        """
        try:
            res = StaffPosition.objects.all().values()
            result_list = list(res)
            result = {"code": True, "result": result_list, "message": u"查询成功"}
        except Exception, e:
            result = {"code": False, "result": None, "message": u"查询失败 %s" % e}
        return result

    def get_staff_position_by_username(self, staff_position_id):
        try:
            res = StaffPosition.objects.get(staff_position_id=staff_position_id)
            dict = res.__dict__
            del dict['_state']
            result = {"code": True, "result": dict, "message": u"查询成功"}
        except Exception, e:
            result = {"code": False, "result": None, "message": u"查询失败 %s" % e}
        return result


class StaffPosition(models.Model):
    """
    员工岗位表
    """
    staff_position_id = models.IntegerField(u'职员岗位ID')
    staff_position_name = models.CharField(u'岗位名称', max_length=64)
    objects = StaffPositionManage()

    def __unicode__(self):
        return self.staff_position_id

    class Meta:
        verbose_name = u'员工岗位表'
        verbose_name_plural = u'员工岗位表'


class StaffSceneManage(models.Manager):
    """
    用户自定义场景设置表管理
    """
    def save_staff_scene(self, data):
        """
        保存用户场景设置
        :param data:
        :return:
        """
        try:
            StaffScene.objects.create(
                bk_username=data.get("bk_username"),
                staff_scene_id=data.get("staff_scene_id"),
                staff_scene_order_id=data.get("staff_scene_order_id"),
                staff_scene_default_time=data.get("staff_scene_default_time"),
            )
            result = {'result': True, 'message': "保存成功"}
        except Exception, e:
            result = {'result': False, 'message': "保存失败 %s" % e}
        return result


class StaffScene(models.Model):
    """
    用户自定义场景设置表
    """
    staff_scene_id = models.IntegerField(u'用户场景ID');
    staff_scene_order_id = models.IntegerField(u'用户场景排序ID')
    bk_username = models.CharField(u'职员用户名', max_length=64)
    staff_scene_default_time = models.CharField(u'场景停留时间', max_length=64)
    objects = StaffSceneManage()

    def __unicode__(self):
        return "%d" % self.int

    class Meta:
        verbose_name = u'员工自定义设置场景信息表'
        verbose_name_plural = u'员工自定义设置场景信息表'


class PositionSceneManage(models.Manager):
    """
        StaffPosition 与 Scene 关系表管理  (多对多)
    """
    def get_position_scene(self, position_id):
        """
        通过职位ID获取对应场景ID
        :param position_id: 职位ID
        :return: PositionScene对象
        """
        try:
            res = PositionScene.objects.filter(staff_position_id=position_id).values()
            result_list = list(res)
            result = {"code": True, "result": result_list, "message": u"查询成功"}
        except Exception, e:
            result = {"code": False, "result": None, "message": u"查询失败 %s" % e}
        return result


class PositionScene(models.Model):
    """
    StaffPosition 与 Scene 关系表  (多对多)
    """
    staff_position_id = models.IntegerField(u'职员岗位ID')
    scene_id = models.IntegerField(u'场景ID')
    objects = PositionSceneManage()

    def __unicode__(self):
        return "%d" % self.int

    class Meta:
        verbose_name = u'岗位与场景关系表'
        verbose_name_plural = u'岗位场景关系表'