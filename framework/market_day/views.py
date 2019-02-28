# -*- coding:utf-8 -*-

from django.shortcuts import render
from shell_app.function import render_json
import function
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
import tasks
from monitor_item import tools
import os
import sys
from logmanagement.function import add_log,make_log_info,get_active_user

def get_holiday(req,area):
    days=function.get_holiday(req,area)
    return render_json(days)
@csrf_exempt
def get_file(req,area):
    path=function.get_file(req,area)
    return HttpResponse('ok')
def send_demo(req,email):
    print email
    tasks.sendemail.delay(email)
    return HttpResponse('success')
def delall(req,area):
    try:
        flag=function.delall(area)
        info = make_log_info(u'删除全部交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             get_active_user(req)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'删除全部交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             get_active_user(req)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return render_json(flag)

def delone(req):
    try:
        function.delone(req)
        info = make_log_info(u'变更为交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             get_active_user(req)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'变更为交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             get_active_user(req)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return render_json('ok')

def addone(req):
    try:
        function.addone(req)
        info = make_log_info(u'取消交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             get_active_user(req)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'取消交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             get_active_user(req)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return render_json('ok')

def get_all_timezone(req):
    res=function.get_all_timezone()
    return render_json(res)
def get_data_header(req):
    function.get_header_data(req)
    return HttpResponse('ok')

def add_area(req):
    res=function.add_area(req)
    return render_json(res)

def get_all_area(req):
    res=function.get_all_area(req)
    return render_json(res)

def del_area(req,name):
    res=function.del_area(name)
    return render_json(res)



