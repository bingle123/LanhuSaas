# -*- coding:utf-8 -*-

from django.shortcuts import render
from shell_app.function import render_json
import function
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
import tasks
from monitor import tools
import os
import sys
from logmanagement.function import add_log,make_log_info,get_active_user

def get_holiday(req):
    days=function.get_holiday(req)
    return render_json(days)
@csrf_exempt
def get_file(req):
    path=function.get_file(req)
    return HttpResponse('ok')
def send_demo(req,email):
    print email
    tasks.sendemail.delay(email)
    return HttpResponse('success')
def delall(req):
    try:
        flag=function.delall(req)
        info = make_log_info(u'删除全部交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             get_active_user(req)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'删除全部交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             get_active_user(req)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return render_json(flag)

def delone(req,date):
    try:
        flag=function.delone(req,date)
        info = make_log_info(u'变更为交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             get_active_user(req)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'变更为交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             get_active_user(req)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return render_json(flag)

def addone(req,date):
    try:
        flag=function.addone(req,date)
        info = make_log_info(u'取消交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             get_active_user(req)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'取消交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             get_active_user(req)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return render_json(flag)

def cedemo(req):
    user_account = BkUser.objects.filter(id=1).get()
    client = get_client_by_user(user_account)
    client.set_bk_api_ver('v2')
    param={
       'monitor_name':'frg',
       'monitor_type':'流程单元类型',
       'template_id':5,
        'node_times':[
            {'starttime':'15:30',
             'endtime':'16:30'
             },
            {'starttime':'15:30',
             'endtime':'16:30'
             }
        ],
        'template_name':'CY流程测试',
        'period':10,
    }
    info = {
        'id': 51,
        'template_id': 5,  # 创建任务的模板id
        'node_times':[
            {'starttime':'15:30',
             'endtime':'16:30'
             },
            {'starttime':'15:30',
             'endtime':'16:30'
             }
        ],
        'template_name': 'CY流程测试',
        'period':100
    }
    param = {
        "bk_biz_id": "2",
        'task_id': 41
    }
    res = client.sops.start_task(param)
    p={"item_id": 51, "node_times": [{"endtime": "16:30", "starttime": "15:30"}, {"endtime": "16:30", "starttime": "15:30"}], "task_id": 31}
    return render_json(res)
def get_data_header(req):
    function.get_header_data(req)
    return HttpResponse('ok')



