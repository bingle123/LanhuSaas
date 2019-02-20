# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from common.mymako import render_json, render_mako_context
import function


def data_base(request):

    return render_mako_context(request, './DataBaseManage/database.html')


#模糊查询
def selecthor(request):
    res = function.selecthor(request)
    return render_json(res)


#查询所有
def getconn(request):

    connall = function.getconn_all(request)
    return render_json(connall)


# 保存
def saveconn(request):
    re = function.saveconn_all(request)
    return render_json(re)


# 修改
def eidtconnn(request):
    re = function.eidtconnn(request)
    return render_json(re)


# 测试
def testConn(request):
    r = function.testConn(request)
    return render_json(r)



def delete_conn(request,id):
    function.delete_conn(request,id)
    return render_json(0)


def delete_conn(request,id):
    function.delete_conn(request,id)
    return render_json(0)



def get_all_db_connection(request):
    """
    获取所有的数据库连接
    :param request:
    :return: json结果集
    """
    res = function.get_all_db_connection(request)
    return render_json(res)


# 获取名称
def get_conname(request):

    res = function.get_conname(request)
    return render_json(res)