# -*- coding: utf-8 -*-
import function
from common.mymako import render_json, render_mako_context
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def index(request):
    return render_mako_context(request, './monitorScene/senceSet.html')
def demo(request):
    return render_mako_context(request, './Demo.html')
def monitor_show(request):
    res = function.monitor_show(request)
    return render_json(res)


def addSence(request):
    res=function.addSence(request)
    return render_json(res)


def select_table(request):
    res=function.select_table(request)
    return  render_json(res)

def delect(request):
    res=function.delect(request)
    return  render_json(res)

def editSence(request):
    res=function.editSence(request)
    return  render_json(res)


def pos_name(request):
    res=function.pos_name(request)
    return  render_json(res)

# 提取编排数据
def scene_data(request):
    id = request.body
    res = function.scene_data(id)
    return render_json(res)

def paging(request):
    res=function.paging(request)
    return  render_json(res)


# 场景编排展示
def scene_show(request):

    param = json.loads(request.body)
    res = function.scene_show(param)
    return render_json(res)
def get_chart_data(req,id):
    res=function.get_chart_data(id)
    return render_json(res)


def get_basic_data(req,id):
    res=function.get_basic_data(id)
    return render_json(res)


def getBySceneId(request,id):
    res = function.getBySceneId(request,id)
    return render_json(res)


def get_scenes(request):
    res = function.get_scenes(request)
    return render_json(res)