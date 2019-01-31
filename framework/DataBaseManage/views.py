# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from common.mymako import render_json, render_mako_context
import function

@csrf_exempt
def data_base(request):

    return render_mako_context(request, './DataBaseManage/database.html')


#模糊查询
@csrf_exempt
def selecthor(request):
    res = function.selecthor(request)
    return render_json(res)


#查询所有
@csrf_exempt
def getconn(request):

    connall = function.getconn_all(request)
    return render_json(connall)


#保存
@csrf_exempt
def saveconn(request):
    re = function.saveconn_all(request)
    return render_json(re)


#修改
@csrf_exempt
def eidtconnn(request):
    re = function.eidtconnn(request)
    return render_json(re)

#测试
@csrf_exempt
def testConn(request):
    r = function.testConn(request)
    return render_json(r)


@csrf_exempt
def delete_conn(request,id):
    function.delete_conn(request,id)
    return render_json(0)