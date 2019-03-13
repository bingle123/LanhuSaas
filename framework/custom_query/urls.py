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
    'custom_query.views',
    (r'^index$', 'show_index'),                                          # 首页
    (r'^select_queries_pagination$', 'select_queries_pagination'),
    (r'^del_query$', 'del_query'),
    (r'^select_query$', 'select_query'),
    (r'^add_query$', 'add_query'),
    (r'^load_all_tables_name$', 'load_all_tables_name'),
    (r'^load_all_fields_name$', 'load_all_fields_name'),
    (r'sql_test','sql_test'),
)
