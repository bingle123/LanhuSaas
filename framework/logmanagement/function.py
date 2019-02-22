# -*- coding: utf-8 -*-
from __future__ import division
from django.db.models import Q
from django.core.paginator import Paginator
from logmanagement.models import *
import datetime
import json

def add_log(info):
    res = info
    r1 = Operatelog.objects.create(log_type=res['log_type'],log_name=res['log_name'],class_name=res['class_name'],method=res['method'],user_name=res['user_name'],succeed=res['succeed'],message=res['message'])
    return r1

def make_log_info(log_type,log_name,class_name,method,user_name,succeed,message):
    info = {
        'log_type':log_type,
        'log_name': log_name,
        'class_name': class_name,
        'method':method,
        'user_name':user_name,
        'succeed':succeed,
        'message':message
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