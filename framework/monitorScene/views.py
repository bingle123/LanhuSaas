import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import function
from common.mymako import render_json, render_mako_context


# Create your views here.

def index(request):

    return render_mako_context(request, './monitorScene/senceSet.html')



@csrf_exempt
def monitor_show(request):
    res = function.monitor_show(request)
    return render_json(res)

@csrf_exempt
def addSence(request):
    res=function.addSence(request)
    return render_json(res)

@csrf_exempt
def select_table(request):
    res=function.select_table(request)
    return  render_json(res)
@csrf_exempt
def delect(request):
    res=function.delect(request)
    return  render_json(res)
@csrf_exempt
def editSence(request):
    res=function.editSence(request)
    return  render_json(res)


@csrf_exempt
def pos_name(request):
    print '123'
    res=function.pos_name(request)
    return  render_json(res)
