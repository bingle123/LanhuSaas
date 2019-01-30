# -*- coding: utf-8 -*-

from django.db import models
# Create your models here.


class TbCustProcess(models.Model):
    node_name = models.CharField(max_length=50, default="", verbose_name=u"节点名称")
    send_content = models.CharField(max_length=1000, default="", verbose_name=u"通知内容")
    seq = models.PositiveIntegerField(verbose_name=u"顺序")
    receivers = models.CharField(max_length=2000, default="", verbose_name=u"通知接收人")

    class Meta:
        db_table = 'tb_cust_process'
