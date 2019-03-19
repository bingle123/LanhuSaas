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
    'position.views',
    (r'^jobM/$', 'index'),  # 首页--服务器选择页面
    (r'^get_tree/$', 'get_tree'),
    (r'^show/$', 'show'),  # 显示数据
    (r'^select_pos/$', 'select_pos'),  # 查询
    (r'^delete/$', 'delete_pos'),  # 删除
    (r'^add_pos/$', 'add_pos'),  # 增加岗位
    (r'^add_person/$', 'add_person'),  # 增加员工
    (r'^edit_pos/$', 'edit_pos'),  # 编辑
    (r'^get_user/$', 'filter_user'),  # 调接口查询所有用户,并筛选
    (r'^synchronize/$', 'synchronize'),  # 调接口查询所有用户,并筛选
    (r'get_active_user', 'get_active_user'),  # 获取当前登陆用户的蓝鲸名
)
