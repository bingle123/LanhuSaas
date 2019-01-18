# -*- coding:utf-8 -*-

from django.shortcuts import render
from shell_app.function import render_json
from zlx import function
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
import os
@csrf_exempt
@cache_page(60*15)
def get_holiday(req,year):
    days=function.get_holiday(req,year)
    return render_json(days)
@csrf_exempt
@cache_page(60*15)
def get_file(req):
    path=function.get_file(req)
    return HttpResponse('ok')



