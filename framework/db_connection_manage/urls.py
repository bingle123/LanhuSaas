# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'db_connection_manage.views',
    (r'^$', 'index'),
    (r'^element/$', 'element'),     # vueAjax测试
    (r'^vuetest/$', 'vue_test'),     # vue测试表单新增页面
    (r'^vue_add/$', 'vue_add'),  # vue测试表单新增页面
)
