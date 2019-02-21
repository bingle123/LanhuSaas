# -*- coding:utf-8 -*-

from django.shortcuts import render
from shell_app.function import render_json
import function
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
import tasks
import os
from shell_app import tools
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
    client=tools.interface_param(req)
    param={
        "bk_biz_id": "2",
        "task_id": "15"
    }
    res=client.sops.get_task_status(param)
    return render_json(res['data']['children'])
def statusdemo(req):
    function.add_unit_task()
    return HttpResponse('ok')



