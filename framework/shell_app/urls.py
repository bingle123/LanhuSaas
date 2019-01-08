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
    'shell_app.views',
    (r'^show_select$', 'show_select'),                                         # 首页--服务器选择页面
    (r'^$', 'main'),                                                # 首页
    (r'^scene/$', 'scene'),                                           # 场景主页
    (r'^scene_carousel/$', 'scene_carousel'),                         # 场景轮播
    (r'^select_host/$', 'select_host'),                             # 查询主机--分页
    (r'^test2/$', 'model_tree_host'),                               # 选择业务下的集群和模块
    (r'^select_module_host/$', 'select_module_host'),               # 查询模板下面的主机信息
    (r'^carousel', 'carousel'),                                     # 跳转到轮播页面
    (r'^get_scene_by_now_time', 'get_scene_by_now_time'),           # 获取当前时间用户场景--暂时未使用
    (r'^get_staff_scene', 'get_staff_scene'),                       # 获取当前用户当前时间所有场景
    (r'position_setting_html', 'position_setting_html'),            # 岗位设置专用页面
    (r'^get_positions_all', 'get_positions_all'),                   # 获取所有岗位对象
    (r'^scene_list', 'scene_list'),                                 # 所有场景列表
    (r'^add_scene/$', 'add_scene'),                                   # 增加场景表单HTML
    (r'^add_scene_form/$', 'add_scene_form'),                         # 增加场景
    (r'^get_json_test', 'get_json_test'),                           # json数据测试URL
)
