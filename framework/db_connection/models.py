# -*- coding: utf-8 -*-
from django.db import models


class Conn(models.Model):
    """
    数据库表单
    """
    connname = models.CharField(u'连接名称', max_length=30)
    type = models.CharField(u'连接类型', max_length=30)
    ip = models.CharField(u'ip地址', max_length=30)
    port = models.CharField(u'端口', max_length=50)
    username = models.CharField(u'用户名', max_length=155)
    databasename = models.CharField(u'数据库名称', max_length=125)
    password = models.CharField(u'密码', max_length=155)
    createname = models.CharField(u'创建人', max_length=64)
    createtime = models.DateTimeField(u'创建时间', auto_now_add=True)
    editname = models.CharField(u'修改人', max_length=64)
    edittime = models.DateTimeField(u'修改时间', auto_now=True)

    class Meta:
        db_table = 'db_connection_conn'


class Muenu(models.Model):
    """
    菜单表
    """
    mname = models.CharField(u'名称', max_length=255)
    url = models.CharField(u'地址', max_length=255)
    pcode = models.IntegerField(u'父级菜单编号')
    mImg = models.CharField(u'图标', max_length=255)
    class Meta:
        db_table = 'db_connection_muenu'


class Role(models.Model):
    """
    角色表
    """
    rname = models.CharField(u'角色', max_length=255)
    rid = models.IntegerField(u'角色Id')

    class Meta:
        db_table = 'db_connection_role'


class rm(models.Model):
    """
    菜单角色关联表
    """
    roleid = models.IntegerField(u'角色id')
    muenuid = models.IntegerField(u'菜单id')

    class Meta:
        db_table = 'db_connection_rm'
