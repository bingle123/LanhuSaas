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
    flag=function.delall(req)
    return render_json(flag)

def delone(req,date):
    flag=function.delone(req,date)
    return render_json(flag)

def addone(req,date):
    flag=function.addone(req,date)
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
def statusdemo(req):
    function.add_unit_task()
    return HttpResponse('ok')



