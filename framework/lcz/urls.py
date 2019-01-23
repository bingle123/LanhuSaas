# -*- coding: utf-8 -*-
from django.conf.urls import patterns


urlpatterns = patterns(
    'lcz.views',
    (r'^data_base/$', 'data_base'),
    (r'^getall/$', 'getconn'),                               #查询所有
    (r'^getDataType/$','getDataType'),
    (r'^saveconn/$','saveconn'),                             #保存
    (r'^editconn/','eidtconnn'),                             #编辑
    (r'^deleteconn/(.+)/$','delete_conn'),                   #删除
    (R'^testConn/$','testConn'),                             #测试连接
)