# -*- coding: utf-8 -*-
import function
from common.mymako import render_json, render_mako_context
import json

# Create your views here.

def index(request):

    return render_mako_context(request, './monitorScene/senceSet.html')



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


def paging(request):
    res=function.paging(request)
    return  render_json(res)


def scene_show(request):

    # res = json.loads(request.body)
    param0 = {
        'limit': 4,
        "page":1,
        "type":0
    }
    param1 = {
        'limit': 4,
        "page":2,
        "type":1
    }
    param2 = {
        'limit': 4,
        "page":2,
        "type": 2
    }
    param3 = {
        'limit': 4,
        "page":2,
        "type": 3
    }
    param4 = {
        'limit': 4,
        "page":2,
        "type":4
    }
    res = function.scene_show(param3)
    return  render_json(res)