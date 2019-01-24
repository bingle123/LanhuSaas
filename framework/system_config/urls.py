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
    'system_config.views',
    (r'^crawl_config_html$', 'crawl_config_html'),                                     # 网页抓取配置首页
    (r'^manage_crawl', 'manage_crawl'),                                                # 网页爬虫配置管理包括新增和修改
    (r'^delete_crawl', 'delete_crawl'),                                                # 网页爬虫配置删除
    # (r'^get_crawl', 'get_crawl'),                                                      # 网页爬虫配置删除
    (r'^crawl', 'crawl'),                                                              # 网页爬虫配置删除


)
