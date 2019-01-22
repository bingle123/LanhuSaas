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
    'jobManagement.views',
    (r'^jobM$', 'index'),                                          # 首页--服务器选择页面
    (r'^job_show/$', 'positonall'),                                 #显示表中所有数据
    (r'^select_job/$', 'select_job'),                               #查询
    (r'^delete/$', 'delete_job'),                                   #删除
    (r'^add_job/$', 'add_job'),                                     #增加岗位
    (r'^add_person/$', 'add_person'),                               #增加员工
    (r'^edit_job/$', 'edit_job'),                                   #编辑
)
