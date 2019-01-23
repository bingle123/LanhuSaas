# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
import json
import time
from monitor import tools
from django.forms.models import model_to_dict
from lcz.models import *
import MySQLdb
import cx_Oracle
import pymssql

#查询所有
def getconn_all(request):
    conninfo = Conn.objects.all()
    res_list = []
    for i in conninfo:
        dic = model_to_dict(i)
        res_list.append(dic)
    return res_list

#获取数据库类型
def getDataType(request):
    dataType = TDataBase.objects.all()
    res_list = []
    for i in dataType:
        dic = model_to_dict(i)
        res_list.append(dic)
    return res_list

#保存
def saveconn_all(request):
    res = json.loads(request.body)
    re = Conn.objects.create(**res)
    return re

#修改
def eidtconnn(request):
    res = json.loads(request.body)
    re1 = Conn.objects.filter(id=res['id']).update(**res)
    return re1

#删除
def delete_conn(request,id):
    try:
        Conn.objects.filter(id=id).delete()
    except Exception as e:
        res1 = tools.error_result(e)
        return res1

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
            return 1
    except Exception as e:
        print e
        return 0







