# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from market_day import views

# 公共URL配置
urlpatterns = patterns(
    '',
    url(r'get_holiday/(.+)', views.get_holiday),
    url(r'get_file/(.+)', views.get_file),
    url(r'delall/(.+)', views.delall),
    url(r'delone', views.delone),
    url(r'addone', views.addone),
    url(r'get_header', views.get_data_header),
    url(r'add_area', views.add_area),
    url(r'get_all_timezone', views.get_all_timezone),
    url(r'get_all_area', views.get_all_area),
    url(r'del_area/(.+)', views.del_area),
    url(r'test', views.test)  # 测试用url
)
