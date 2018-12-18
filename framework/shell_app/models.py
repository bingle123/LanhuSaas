# -*- coding: utf-8 -*-
from django.db import models

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


class UserCarouselBaseSettingManage(models.Manager):
    def get_carousel(self, data):
        """
        获取用户Carousel设置
        :return:    json
        """
        try:
            res = UserCarouselBaseSetting.objects.get(bk_username=data)
            dict = res.__dict__
            del dict['_state']
            result = {"code": True, "result": dict, "message": u"查询成功"}

        except Exception, e:
            result = {"code": False, "result": None, "message": u"查询失败 %s"% e}
        return result

    def save_carousel(self, data):
        """
        保存用户Carousel设置
        :param data:
        :return:
        """
        try:
            UserCarouselBaseSetting.objects.create(
                bk_username=data.get("bk_username"),
                carousel_time=data.get("carousel_time"),
                carousel_number=data.get("carousel_number"),
                carousel_id=data.get("carousel_id"),

            )
            result = {'result': True, 'message': "保存成功"}
        except Exception, e:
            result = {'result': False, 'message': "保存失败 %s" % e}
        return result

    def update_carousel(self, bk_username, data):
        """
        更新用户Carousel设置
        :param data:
        :return:
        """
        try:
            obj = UserCarouselBaseSetting.objects.get(bk_username=bk_username)
            obj.carousel_time = data.get("carousel_time")
            obj.carousel_number = data.get("carousel_number")
            obj.save()
            result = {'result': True, 'message': "更新成功"}
        except Exception, e:
            result = {'result': False, 'message': "更新失败 %s" % e}
        return result


class UserCarouselBaseSetting(models.Model):
    """
    用户轮播基础设置
    """
    bk_username = models.CharField(u'用户名', max_length=64)
    carousel_time = models.CharField(u'轮播时间_毫秒', max_length=256)
    carousel_number = models.IntegerField(u'轮播数量')
    carousel_id = models.CharField(u'轮播ID', max_length=64)
    objects = UserCarouselBaseSettingManage()

    def __unicode__(self):
        return self.bk_username

    class Meta:
        verbose_name = u'用户轮播设置'
        verbose_name_plural = u'用户轮播设置'


