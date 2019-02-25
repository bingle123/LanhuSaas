# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from common.mymako import render_json, render_mako_context
import function


def data_base(request):

    return render_mako_context(request, './db_connection/database.html')

#菜单管理
def muenu_manage(request):
    return render_mako_context(request, './db_connection/muenu_manage.html')

#模糊查询
def selecthor(request):
    res = function.selecthor(request)
    return render_json(res)

#模糊查询2
def selecthor2(request):
    res = function.selecthor2(request)
    return render_json(res)


# 保存
def saveconn(request):
    re = function.saveconn_all(request)
    return render_json(re)


# 修改
def editconn(request):
    re = function.editconn(request)
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

#获取所有菜单mname
def get_user_muenu(request):
    res = function.get_user_muenu(request)
    return render_json(res)





#新增菜单
def addmuenus(request):
    res = function.addmuenus(request)
    return render_json(res)


#修改菜单
def edit_muenu(request):
    res = function.edit_muenu(request)
    return render_json(res)



#删除菜单
def delete_muenu(request,id):
    res = function.delete_muenu(request,id)
    return render_json(res)



# 获取名称
def get_conname(request):
    res = function.get_conname(request)
    return render_json(res)

# 获取所有角色对应菜单
def get_roleAmuenus(request):
    res = function.get_roleAmuenus(request)
    return render_json(res)

# 获取勾选id
def checked_menu(request):
    res = function.checked_menu(request)
    return render_json(res)

# 获取勾选id
def savemnus(request):
    res = function.savemnus(request)
    print res
    return render_json(res)
