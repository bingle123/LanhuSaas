# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from django.conf.urls import patterns


urlpatterns = patterns(
    'history_chart.views',
    (r'^$', 'index'),                                         # 首页--服务器选择页面
    (r'^show_all/$', 'show_all'),                                    #显示所有操作日志
    (r'^select_log/$', 'select_log'),
    (r'^select_all_rules$', 'select_all_rules'),
    (r'^select_rules_pagination$', 'select_rules_pagination'),
    (r'^select_Keyword', 'select_Keyword'),
    (r'^show_operation_report', 'show_operation_report'),         #查询场景运行情况
    (r'^get_week', 'get_week'),                                     #场景周运行情况
    (r'^about_select', 'about_select'),
    (r'^about_search', 'about_search'),
    (r'^monthly_select', 'monthly_select'),

    (r'^select_scenes/$', 'select_scenes'),     #场景对比分析
    (r'^selectScenes_ById/$', 'selectScenes_ById'),  #选择场景比对



)
