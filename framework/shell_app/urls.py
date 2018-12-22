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
    (r'^$', 'show_select'),
    (r'^test/$', 'show_host'),
    (r'^test2/$', 'model_tree_host'),
    (r'^test1/$', 'select_module_host'),
    (r'^carousel', 'carousel'),
    (r'^user_carousel_setting', 'user_carousel_setting'),
    (r'^get_user_carousel_time', 'get_user_carousel_time'),
    (r'^get_scene_by_now_time', 'get_scene_by_now_time'),
    (r'position_setting_html', 'position_setting_html'),
    (r'^get_json_test', 'get_json_test'),
    (r'^jobtest', 'test'),
)
