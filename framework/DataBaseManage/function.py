# -*- coding: utf-8 -*-
from __future__ import division
import json
import time
from django.forms.models import model_to_dict
from DataBaseManage.models import *
from framework.shell_app import tools
import MySQLdb
import cx_Oracle
import pymssql
import datetime
import base64
import pyDes
from django.db.models import Q
from django.core.paginator import Paginator

Key = "YjCFCmtd"
Iv = "yJXYwjYD"
#加密
def encryption_str(str):
    password = str.encode(encoding='utf-8')
    method = pyDes.des(Key, pyDes.CBC, Iv, pad=None, padmode=pyDes.PAD_PKCS5)
    # 执行加密码
    k = method.encrypt(password)
    # 转base64编码并返回
    return base64.b64encode(k)


#解密
def decrypt_str(data):
    password = data.encode(encoding='utf-8')
    method = pyDes.des(Key, pyDes.CBC, Iv, pad=None, padmode=pyDes.PAD_PKCS5)
    # 对base64编码解码
    k = base64.b64decode(password)
    # 再执行Des解密并返回
    return method.decrypt(k)



#模糊查询
def selecthor(request):
    res = json.loads(request.body)
    search = res['search']
    page = res['page']
    limit = res['limit']
    sciencenews = Conn.objects.filter(Q(connname__contains=search)|Q(type__contains=search)|Q(ip__contains=search)\
                                      |Q(port__contains=search)|Q(username__contains=search)|Q(databasename__contains=search))
    p = Paginator(sciencenews, limit)
    count = p.page_range
    pages = count[-1]

    curren_page = p.page(page)
    objs = []
    for cur in curren_page.object_list:
        conn = model_to_dict(cur)
        conn['count'] = pages
        objs.append(conn)
    return objs

#查询所有
def getconn_all(request):
    res = json.loads(request.body)
    page = res['page']
    limit = res['limit']
    conn = Conn.objects.all()
    p = Paginator(conn, limit)
    count = p.page_range
    pages = count[-1]
    objs=[]
    current_page = p.page(page)
    for cur in current_page.object_list:
        conn=model_to_dict(cur)
        conn['count'] = pages
        objs.append(conn)
    return objs


#保存
def saveconn_all(request):
    try:
        res = json.loads(request.body)
        cilent = tools.interface_param(request)
        user = cilent.bk_login.get_user({})
        res['createname'] = user['data']['bk_username']
        res['editname'] = user['data']['bk_username']

        password = encryption_str(res['password'])
        res['password'] = password
        re = Conn(**res).save()
        return tools.success_result(re)
    except Exception as e:
        res1 = tools.error_result(e)
        return res1



#修改
def eidtconnn(request):
    try:
        res = json.loads(request.body)
        res.pop('page_count')
        print res
        cilent = tools.interface_param(request)
        user = cilent.bk_login.get_user({})
        res['editname'] = user['data']['bk_username']
        res['edittime'] = datetime.datetime.now()

        password = encryption_str(res['password'])
        res['password'] = password
        re1 = Conn.objects.filter(id=res['id']).update(**res)
        return tools.success_result(re1)
    except Exception as e:
        res1 = tools.error_result(e)
        return res1

#删除
def delete_conn(request,id):
    try:
        res = Conn.objects.filter(id=id).delete()
        return tools.success_result(res)
    except Exception as e:
        res1 = tools.error_result(e)
        return tools.error_result(res1)

#测试
def testConn(request):
    res = json.loads(request.body)
    ip = str(res['ip'])
    port = res['port']
    username = res['username']
    password = res['password']
    databasename = res['databasename']
    try:
        if res['type'] == 'MySQL':
            db = MySQLdb.connect(host=ip, user=username, passwd=password, db=databasename, port=int(port))
        elif res['type'] == 'Oracle':
            sql=r'%s/%s@%s/%s'%(username,password,ip,databasename)
            db = cx_Oracle.connect(sql)
        else:
            db = pymssql.connect(host = ip+r':'+port,user =username,password = password,database = databasename)

        cursor = db.cursor()
        if cursor != '':
            cursor.close()
            db.close()
            return tools.success_result(cursor)
    except Exception as e:
        return tools.error_result(e)







