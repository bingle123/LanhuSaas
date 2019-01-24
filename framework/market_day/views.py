# -*- coding:utf-8 -*-

from django.shortcuts import render
from shell_app.function import render_json
from market_day import function
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
import tasks
import os
@csrf_exempt
def get_holiday(req):
    days=function.get_holiday(req)
    return render_json(days)
@csrf_exempt
def get_file(req):
    path=function.get_file(req)
    return HttpResponse('ok')
@csrf_exempt
def send_demo(req,email):
    print email
    tasks.sendemail.delay(email)
    return HttpResponse('success')
@csrf_exempt
def delall(req):
    flag=function.delall(req)
    return render_json(flag)

@csrf_exempt
def delone(req,date):
    flag=function.delone(req,date)
    return render_json(flag)

@csrf_exempt
def addone(req,date):
    flag=function.addone(req,date)
    return render_json(flag)




