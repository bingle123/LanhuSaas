# -*- coding: utf-8 -*-

from django.db import models


class TbCustQuery(models.Model):
    conn_id = models.CharField(max_length=10, verbose_name=u"数据库连接ID")
    query_name = models.CharField(max_length=50, verbose_name=u"查询名称")
    show_type = models.CharField(max_length=50, verbose_name=u"展示方式")
    query_sql = models.CharField(max_length=1000, verbose_name=u"自定义查询sql")

    class Meta:
        db_table = 'tb_cust_query'
