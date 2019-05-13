# -*- coding: utf-8 -*-
from django.conf.urls import patterns

urlpatterns = patterns(
    'home_page.views',
    (r'^get_time/$', 'get_time'),  # 获取时间
    (r'^scenes_alert', 'scenes_alert'),  # 场景告警
    (r'scenes_item_list','scenes_item_list'), # 单个场景监控项
    (r'^select_all', 'select_all'),  # 系统运行
    # (r'^get_scene','get_scene'),
)
