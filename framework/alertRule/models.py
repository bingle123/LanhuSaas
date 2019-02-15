# -*- coding: utf-8 -*-

from django.db import models


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
告警消息订阅表
class TlAlertUser(models.Model):
    rule_id=models.ForeignKey(TbAlertRule) #规则外键
    user_id=models.ForeignKey('jobManagement.Localuser') #用户外键

    class Meta:
        db_table='tl_alert_user'

#发送告警信息日志
class TdAlertLog(models.Model):
    rule_id=models.IntegerField(null=True, verbose_name=u"告警规则id")
    item_id = models.PositiveIntegerField(verbose_name=u"监控项ID")
    alert_title = models.CharField(max_length=100, verbose_name=u"告警标题")
    alert_content = models.CharField(max_length=2000, verbose_name=u"告警内容")
    alert_time = models.DateTimeField(verbose_name=u"告警时间", auto_now_add=True)
    persons=models.CharField(max_length=1000,verbose_name=u"给谁发的")

    class Meta:
        db_table='td_alert_log'

