# -*- coding: utf-8 -*-
from __future__ import division
from django.db.models import Q
from django.core.paginator import Paginator
from logmanagement.models import *
import datetime
import json
from shell_app import tools


def add_log(info):
    res = info
    r1 = Operatelog.objects.create(log_type=res['log_type'], log_name=res['log_name'], class_name=res['class_name'],
                                   method=res['method'], user_name=res['user_name'], succeed=res['succeed'],
                                   message=res['message'])
    return r1


def make_log_info(log_type, log_name, class_name, method, user_name, succeed, message):
    """
    :param log_type: 操作类型
    :param log_name:日志名称
    :param class_name:类名称
    :param method:方法名称
    :param user_name:用户名称
    :param succeed:是否成功
    :param message:备注
    :return:
    """
    info = {
        'log_type': log_type,
        'log_name': log_name,
        'class_name': class_name,
        'method': method,
        'user_name': user_name,
        'succeed': succeed,
        'message': message
    }
    return info


def get_active_user(request):
    """
    通过蓝鲸获取当前用户
    :param request:
    :return:            dict
    """
    client = tools.interface_param(request)
    res = client.bk_login.get_user({})
    return res


def show_all(request):
    """
        显示所有操作日志
    """
    res = json.loads(request.body)
    limit = res['limit']
    page = res['page']
    log = Operatelog.objects.all()
    p = Paginator(log, limit)
    count = p.page_range
    pages = count[-1]
    res_list = []
    current_page = p.page(page)
    for x in current_page:
        dic = {
            'id': x.id,
            'log_type': x.log_type,
            'log_name': x.log_name,
            'user_name': x.user_name,
            'class_name': x.class_name,
            'method': x.method,
            'create_time': str(x.create_time),
            'succeed': x.succeed,
            'message': x.message,
            'page_count': pages
        }
        res_list.append(dic)
    return res_list


def select_log(request):
    res = json.loads(request.body)
    limit = res['limit']
    page = res['page']
    search = res['search'].strip()
    res1 = search
    res_list = []
    tmp = Operatelog.objects.all()
    log = tmp.filter(Q(log_type__icontains=res1) | Q(log_name__icontains=res1) | Q(user_name__icontains=res1) | Q(
        class_name__icontains=res1) | Q(method__icontains=res1))
    p = Paginator(log, limit)
    count = p.page_range
    pages = count[-1]
    current_page = p.page(page)
    for x in current_page:
        dic = {
            'id': x.id,
            'log_type': x.log_type,
            'log_name': x.log_name,
            'user_name': x.user_name,
            'class_name': x.class_name,
            'method': x.method,
            'create_time': str(x.create_time),
            'succeed': x.succeed,
            'message': x.message,
            'page_count': pages
        }
        res_list.append(dic)
    return res_list
