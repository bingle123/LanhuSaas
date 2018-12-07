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

