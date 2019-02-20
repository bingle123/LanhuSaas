# -*- coding: utf-8 -*-
from django.conf.urls import patterns


urlpatterns = patterns(
    'DataBaseManage.views',
    (r'^data_base/$', 'data_base'),
    (r'^getall/$', 'getconn'),                               #查询所有
    (r'^saveconn/$','saveconn'),                             #保存
    (r'^editconn/$','eidtconnn'),                             #编辑
    (r'^deleteconn/(.+)/$','delete_conn'),                   #删除
    (r'^testConn/$','testConn'),                             #测试连接
    (r'^selecthor/$','selecthor'),                          #模糊查询
    (r'^get_all_db_connection/$','get_all_db_connection'),                          # 获取所有的数据库连接
    (r'^get_conname/$','get_conname'),                       #获取名称
)