# encoding:utf-8
from django.db import models


# Create your models here.
class CrawlerConfig(models.Model):
    """
    网页爬虫配置
    """
    crawl_name = models.CharField(verbose_name=u'爬虫名称', max_length=64)
    crawl_url = models.CharField(verbose_name=u'爬虫地址URL', max_length=128)
    crawl_keyword = models.CharField(verbose_name=u'关键字', max_length=64)
    crawl_no_keyword = models.CharField(verbose_name=u'非关键字', max_length=64)  # 可设置多个，用逗号隔开
    period = models.CharField(verbose_name=u'爬虫周期', max_length=64)
    url_pre = models.CharField(verbose_name=u'静态资源前缀', max_length=64)
    total_xpath = models.CharField(verbose_name=u'总Xpath', max_length=255)
    title_xpath = models.CharField(verbose_name=u'标题Xpath', max_length=64)
    time_xpath = models.CharField(verbose_name=u'时间Xpath', max_length=64)
    url_xpath = models.CharField(verbose_name=u'URLXpath', max_length=64)
    create_user = models.CharField(verbose_name=u'创建人', max_length=64)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)  # 新建后无法更改
    update_user = models.CharField(verbose_name=u'最后修改用户', max_length=64)
    update_time = models.DateTimeField(verbose_name=u'最后修改时间', auto_now=True)  # 跟新数据库，字段自动更新
    receivers = models.TextField(verbose_name=u'通知人')  # 通知人, 可设置多个人用@隔开


class CrawlContent(models.Model):
    """
    爬取内容表
    """
    crawl_id = models.IntegerField(verbose_name=u'爬虫配置ID')  # 与爬虫配置ID关联
    title_content = models.CharField(verbose_name=u'标题内容', max_length=64)
    time_content = models.CharField(verbose_name=u'时间内容', max_length=64)
    url_content = models.CharField(verbose_name=u'资源内容', max_length=255)
    save_time = models.DateTimeField(verbose_name=u'保存时间', auto_now_add=True)


class SendMailLog(models.Model):
    """
    信息发送日志表
    """
    link_id = models.IntegerField(verbose_name=u'关联id')
    message_type = models.CharField(max_length=100, verbose_name=u'消息的类型', default='crawl')  # 默认为爬虫消息日志
    message_title = models.CharField(max_length=200, verbose_name=u'消息的标题')
    message_content = models.CharField(max_length=1000, verbose_name=u'消息的内容')
    send_time = models.DateTimeField(verbose_name=u'消息发送的时间', auto_now_add=True)


class SceneType(models.Model):
    """
    场景类型表
    """
    scene_type_id = models.CharField(verbose_name=u'场景UUID', max_length=128)
    scene_type_name = models.CharField(verbose_name=u'场景类型名称', max_length=64)
    create_user = models.CharField(verbose_name=u'创建人', max_length=64)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)  # 新建后无法更改
    update_user = models.CharField(verbose_name=u'最后修改用户', max_length=64)
    update_time = models.DateTimeField(verbose_name=u'最后修改时间', auto_now=True)  # 跟新数据库，字段自动更新
    start_time = models.TimeField(verbose_name=u'开始时间')
    stop_time = models.TimeField(verbose_name=u'结束时间')

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = u'场景分组'
        verbose_name_plural = u'场景分组'
        db_table = "system_config_scenetype"

class SysBoard(models.Model):
    """
    看板标题表
    """
    id =  models.IntegerField(u'ID', primary_key=True, auto_created=True)
    boardTitle = models.CharField(verbose_name=u'看板项目名称', max_length=255)

    class Meta:
        db_table = 'sys_board'