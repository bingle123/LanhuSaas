# -*- coding: utf-8 -*-

from django.db import models
# Create your models here.


class TbAlertRule(models.Model):
    item_id = models.PositiveIntegerField(verbose_name=u"监控项ID")
    key_name = models.CharField(max_length=50, verbose_name=u"数据key名称")
    rule_name = models.CharField(max_length=50, verbose_name=u"规则名称")
    upper_limit = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=u"上限值", null=True)
    lower_limit = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=u"下限值", null=True)
    alert_title = models.CharField(max_length=100, verbose_name=u"告警标题")
    alert_content = models.CharField(max_length=2000, verbose_name=u"告警内容")
    create_time = models.DateTimeField(verbose_name=u"创建时间")
    creator = models.CharField(max_length=50, verbose_name=u"创建人")
    edit_time = models.DateTimeField(verbose_name=u"修改时间")
    editor = models.CharField(max_length=50, verbose_name=u"修改人")

    class Meta:
        db_table = 'tb_alert_rule'
