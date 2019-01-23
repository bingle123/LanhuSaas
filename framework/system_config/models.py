# encoding:utf-8
from django.db import models


# Create your models here.
class CrawlerConfig(models.Model):
    """
    网页爬虫配置
    """
    crawl_name = models.CharField(verbose_name=u'爬虫名称', max_length=64)
    crawl_url = models.CharField(verbose_name=u'爬虫地址URL', max_length=64)
    crawl_keyword = models.CharField(verbose_name=u'关键字', max_length=64)
    crawl_no_keyword = models.CharField(verbose_name=u'非关键字', max_length=64)  # 可设置多个，用逗号隔开
    create_user = models.CharField(verbose_name=u'创建人', max_length=64)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)        # 新建后无法更改
    update_user = models.CharField(verbose_name=u'最后修改用户', max_length=64)
    update_time = models.DateTimeField(verbose_name=u'最后修改时间', auto_now=True)        # 跟新数据库，字段自动更新
    notifier = models.CharField(verbose_name=u'通知人', max_length=64)  # 通知人, 可设置多个人用逗号隔开

    class Meta:
        db_table = 'system_config_crawler'  # 数据库表名
        get_latest_by = 'update_time'       # 排序字段