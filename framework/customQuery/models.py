# -*- coding: utf-8 -*-

from django.db import models


class TbCustQuery(models.Model):
    conn_id = models.CharField(max_length=10, verbose_name=u"数据库连接ID")
    query_name = models.CharField(max_length=50, verbose_name=u"查询名称")
    show_type = models.CharField(max_length=50, verbose_name=u"展示方式")
    table_name = models.CharField(max_length=50, verbose_name=u"选择表名")
    show_fields = models.CharField(max_length=2000, verbose_name=u"显示字段")
    fields_prop = models.CharField(max_length=4000, verbose_name=u"字段属性")
    x_name = models.CharField(max_length=50, verbose_name=u"x轴字段名", null=True)
    y_name = models.CharField(max_length=50, verbose_name=u"y轴字段名", null=True)
    query_sql = models.CharField(max_length=1000, verbose_name=u"自定义查询sql")

    class Meta:
        db_table = 'tb_cust_query'
