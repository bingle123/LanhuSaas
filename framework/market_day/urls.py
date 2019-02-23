# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from market_day import views
# 公共URL配置
urlpatterns = patterns(
    '',
    url(r'get_holiday/',views.get_holiday),
    url(r'get_file/',views.get_file),
    url(r'celerydemo/(.+)',views.send_demo),
    url(r'delall/',views.delall),
    url(r'delone/(.+)',views.delone),
    url(r'addone/(.+)',views.addone),
    url(r'get_header',views.get_data_header)
)

