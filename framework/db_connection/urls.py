# -*- coding: utf-8 -*-
from django.conf.urls import patterns

urlpatterns = patterns(
    'db_connection.views',
    (r'^data_base/$', 'data_base'),
    (r'^saveconn/$', 'save_conn'),  # 保存数据库链接
    (r'^editconn/$', 'edit_conn'),  # 编辑数据库链接
    (r'^deleteconn/(.+)/$', 'delete_conn'),  # 删除数据库链接
    (r'^testConn/$', 'test_conn'),  # 测试连接
    (r'^selecthor/$', 'selecthor'),  # 模糊查询
    (r'^get_all_db_connection/$', 'get_all_db_connection'),  # 获取所有的数据库连接
    (r'^muenu_manage/$', 'menu_manage'),  # 菜单管理页面
    (r'^get_user_muenu/$', 'get_user_menu'),  # 根据角色获取菜单
    (r'^selecthor2/$', 'selecthor2'),  # 分页获取
    (r'^addmuenus/$', 'add_menu'),  # 增加菜单
    (r'^edit_muenu/$', 'edit_menu'),  # 编辑菜单
    (r'^delete_muenu/(.+)/$', 'delete_menu'),  # 删除菜单
    (r'^get_conname/$', 'get_conname'),  # 获取名称
    (r'^get_roleAmuenus/$', 'get_roleAmuenus'),  # 获取所有角色对应菜单
    (r'^checked_menu/$', 'checked_menu'),
    (r'^savemnus/$', 'save_menu'),
    (r'^get_all_mImgs/$', 'get_all_mImgs'),
)
