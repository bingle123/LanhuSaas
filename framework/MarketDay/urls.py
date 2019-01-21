# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from MarketDay import views
# 公共URL配置
urlpatterns = patterns(
    '',
    url(r'^get_holiday/(.+)/$',views.get_holiday),
    url(r'get_file/',views.get_file)
)

