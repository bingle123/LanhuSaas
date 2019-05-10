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
    'monitor_scene.views',
    (r'^$', 'index'),  # 首页--服务器选择页面
    (r'demo', 'demo'),
    (r'^monitor_show/$', 'monitor_show'),
    (r'^addSence/$', 'addSence'),
    (r'^select_table/$', 'select_table'),
    (r'^del_scene/$', 'delete_scene'),
    (r'^editSence/$', 'editSence'),
    (r'^pos_name/$', 'pos_name'),
    (r'^paging/$', 'paging'),
    (r'^scene_show/$', 'scene_show'),  # 场景展示
    (r'get_chart_data/(.+)$', 'get_chart_data'),
    (r'^getSceneByid/(.+)/$', 'getBySceneId'),  # 根据Id获取场景详情
    (r'get_basic_data/(.+)$', 'get_basic_data'),
    (r'^alternate_play/$', 'alternate_play'),
    (r'^alternate_play_test', 'alternate_play_test'),
    (r'query_pos_scene', 'query_pos_scene'),  # 根据岗位id查询场景
    (r'query_curr_user_scene', 'query_curr_user_scene'),  # 查询当前用户场景
    (r'^scene_data/$', 'scene_data'),
    (r'^monitor_scene_show/$', 'monitor_scene_show'),
    (r'^get_all_pos/$', 'get_all_pos'),
    (r'^scene_color_save/$', 'scene_color_save'),
    (r'^scene_color_get/$', 'scene_color_get'),
    (r'^scene_color_del/$', 'scene_color_del'),
    (r'^load_flow_graph/$', 'load_flow_graph'),
    (r'^edit_flow_graph/$', 'edit_flow_graph'),
    (r'^is_monitor_item_collect/$', 'is_monitor_item_collect'),
    (r'^monitor_scene_fuzzy_search/$', 'monitor_scene_fuzzy_search'),
    (r'^save/$', 'save_scene_design'),
    (r'^open/$', 'open_win'),
    (r'^open_scene_design/$', 'query_scene_design'),
    (r'^page_query_scene/$', 'page_query_scene'),
    (r'page_query_xml_show', 'page_query_xml_show'),  # 展示页面流程图
    (r'query_scene_item_data', 'query_scene_item_data'),  # 监控项的id查询监控值与颜色用于流程展示
)
