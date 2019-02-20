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
    (r'^muenu_manage/$', 'muenu_manage'),       #菜单管理页面
    (r'^get_user_muenu/$', 'get_user_muenu'),           #根据角色获取菜单
    (r'^get_all_muenu/$', 'get_all_muenu'),           #获取所有菜单
    (r'^selecthor2/$','selecthor2'),                          #模糊查询
    (r'^addmuenus/$', 'addmuenus'),       #增加菜单
    (r'^edit_muenu/$', 'edit_muenu'),       #编辑菜单
    (r'^delete_muenu/(.+)/$', 'delete_muenu'),       #删除菜单
    (r'^get_conname/$','get_conname'),                       #获取名称
)