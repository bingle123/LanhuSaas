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
    'monitorScene.views',
    (r'^$', 'index'),# 首页--服务器选择页面
    (r'demo', 'demo'),
    (r'^monitor_show/$', 'monitor_show'),
    (r'^addSence/$', 'addSence'),
    (r'^select_table/$', 'select_table'),
    (r'^delect/$', 'delect'),
    (r'^editSence/$', 'editSence'),
    (r'^pos_name/$', 'pos_name'),
    (r'^paging/$', 'paging'),
    (r'^scene_show/$', 'scene_show'),                        #场景展示
    (r'^add_scene/$', 'add_scene'),                         #场景保存
    (r'get_chart_data/(.+)$','get_chart_data'),
    (r'^getSceneByid/(.+)/$','getBySceneId'),   #根据Id获取场景详情
    (r'get_basic_data/(.+)$','get_basic_data'),
    (r'^get_scenes/$', 'get_scenes'),
    (r'^alternate_play/$', 'alternate_play'),
    (r'^alternate_play_test/$', 'alternate_play_test'),
)
