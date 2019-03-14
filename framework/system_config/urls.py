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
    (r'^crawl_config_html$', 'crawl_config_html'),                                      # 网页抓取配置首页
    (r'^scene_type_html$', 'scene_type_html'),                                      # 网页抓取配置首页
    (r'^crawl_content_html', 'crawl_content_html'),                                      # 网页抓取配置首页
    (r'^manage_crawl', 'manage_crawl'),                                                 # 网页爬虫配置管理包括新增和修改
    (r'^delete_crawl', 'delete_crawl'),                                                 # 网页爬虫配置删除
    (r'^get_crawls/', 'get_crawls'),                                                    # 获取爬虫信息
    (r'^get_crawl_by_name/', 'get_crawl_by_name'),                                      # 通过crawl名字获取爬虫配置
    (r'^crawl/$', 'crawl'),                                                             # 网页爬虫配置删除
    (r'^start_crawl', 'start_crawl'),                                                   # 开始爬虫
    (r'^crawl_test/$', 'crawl_test'),                                                   # 开始爬虫
    (r'^mail_send', 'mail_send'),                                                       # 发送邮件
    (r'^get_scene_type/$', 'get_scene_type'),                                           # 获取场景类型
    (r'^add_scene_type/$', 'add_scene_type'),                                           # 新增场景类型
    (r'^edit_scene_type_by_uuid/$', 'edit_scene_type_by_uuid'),                         # 修改场景类型
    (r'^delete_scene_by_uuid/$', 'delete_scene_by_uuid'),                                     # 删除场景类型
    (r'^get_crawl_content/$', 'get_crawl_content'),                                     # 删除场景类型
    (r'^start_crawl_test/$', 'start_crawl_test'),                                     # 删除场景类型
    (r'^json_test', 'json_test'),   # 测试专用
    (r'^test', 'test'),   # 测试专用

)
