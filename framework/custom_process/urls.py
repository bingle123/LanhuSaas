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
    'custom_process.views',
    (r'^index$', 'show_index'),                                          # 首页
    (r'^select_all_nodes$', 'select_all_nodes'),                         # 查询所有节点信息
    (r'^add_node$', 'add_node'),                                         # 添加流程节点
    (r'^update_node_status$', 'update_node_status'),                     # 更新节点状态信息
    (r'^change_status_flag$', 'change_status_flag'),                     # 变更节点执行状态
    (r'^del_node$', 'del_node'),                                         # 删除节点信息
    (r'^select_node$', 'select_node'),                                   # 根据id获取节点信息
    (r'^truncate_node$', 'truncate_node'),                               # 删除所有节点信息
    (r'^clear_execute_status$', 'clear_execute_status'),                 # 清除所有节点的状态信息
    (r'^select_all_bkusers$', 'select_all_bkusers'),                     # 获取所有的蓝鲸用户信息
    (r'^send_notification$', 'send_notification'),                       # 节点执行完毕发送通知
    (r'^select_nodes_pagination$', 'select_nodes_pagination'),            # 分页获取指定页节点信息
    (r'^get_custom_process_info$', 'get_custom_process_info')            # 获取所有自定义流程节点信息
)
