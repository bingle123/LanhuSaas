# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from common.mymako import render_json, render_mako_context
import function

@csrf_exempt
def data_base(request):

    return render_mako_context(request, './DataBaseManage/database.html')

#菜单管理
@csrf_exempt
def muenu_manage(request):
    return render_mako_context(request, './DataBaseManage/muenu_manage.html')

#模糊查询
@csrf_exempt
def selecthor(request):
    res = function.selecthor(request)
    return render_json(res)

#模糊查询2
@csrf_exempt
def selecthor2(request):
    res = function.selecthor2(request)
    return render_json(res)


#查询所有
@csrf_exempt
def getconn(request):

    connall = function.getconn_all(request)
    return render_json(connall)


# 保存
@csrf_exempt
def saveconn(request):
    re = function.saveconn_all(request)
    return render_json(re)


# 修改
@csrf_exempt
def eidtconnn(request):
    re = function.eidtconnn(request)
    return render_json(re)


# 测试
@csrf_exempt
def testConn(request):
    r = function.testConn(request)
    return render_json(r)


@csrf_exempt
def delete_conn(request,id):
    function.delete_conn(request,id)
    return render_json(0)


@csrf_exempt
def get_all_db_connection(request):
    """
    获取所有的数据库连接
    :param request:
    :return: json结果集
    """
    res = function.get_all_db_connection(request)
    return render_json(res)

#获取所有菜单mname
@csrf_exempt
def get_user_muenu(request):
    res = function.get_user_muenu(request)
    return render_json(res)




#获取所有菜单
@csrf_exempt
def get_all_muenu(request):
    res = function.get_all_muenu(request)
    return render_json(res)




#新增菜单
@csrf_exempt
def addmuenus(request):
    res = function.addmuenus(request)
    return render_json(res)


#修改菜单
@csrf_exempt
def edit_muenu(request):
    res = function.edit_muenu(request)
    return render_json(res)



#删除菜单
@csrf_exempt
def delete_muenu(request,id):
    res = function.delete_muenu(request,id)
    return render_json(res)

