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
    'customProcess.views',
    (r'^index$', 'show_index'),                                          # 首页
    (r'^select_all_nodes$', 'select_all_nodes'),
    (r'^add_node$', 'add_node'),
    (r'^update_node_status', 'update_node_status'),
    (r'^change_status_flag', 'change_status_flag'),
    (r'^del_node', 'del_node'),
    (r'^select_node', 'select_node'),
    (r'^truncate_node', 'truncate_node'),
    (r'^clear_execute_status', 'clear_execute_status'),
)
