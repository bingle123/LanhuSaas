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
from db_connection.models import Conn
from pyDes import *
from binascii import b2a_hex,a2b_hex
import base64
import pyDes
import math

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
    try:

        res = json.loads(request.body)
        limit = res['limit']  # 5
        page = res['page']  # 1
        search = res['search']
        start_page = limit * page - 4  # 开始1



        res_list = []
        res1 = search
        print res1
        if len(res1) == 0:
            res_list = getconn_all(request)
        else:
            if res1.isdigit():
                if Conn.objects.filter(id=int(res1)).exists():
                    unit = Conn.objects.filter(id=int(res1))
            if Conn.objects.filter(connname=res1).exists():
                unit = Conn.objects.filter(connname=res1)
            if Conn.objects.filter(type=res1).exists():
                unit = Conn.objects.filter(type=res1)
            if Conn.objects.filter(ip=res1).exists():
                unit = Conn.objects.filter(ip=res1)
            if Conn.objects.filter(port=res1).exists():
                unit = Conn.objects.filter(port=res1)
            if Conn.objects.filter(username=res1).exists():
                unit = Conn.objects.filter(username=res1)

            totals = unit.values('id')  # 总条数
            page_count = math.ceil(len(totals) / 5)
            unit2 = unit[start_page-1:start_page+4]
            for i in unit2:
                dic = {
                    'id': i.id,
                    'connname': i.connname,
                    'type': i.type,
                    'ip': i.ip,
                    'port': i.port,
                    'username': i.username,
                    'databasename': i.databasename,
                    'password': i.password,
                    'createname': i.createname,
                    'createtime': str(i.createtime),
                    'editname': i.editname,
                    'edittime': str(i.edittime),
                    'page_count': page_count,
                }
                res_list.append(dic)
        return res_list
    except Exception as e:
        return None


#查询所有
def getconn_all(request):
    res = json.loads(request.body)
    limit = res['limit']  # 5
    page = res['page']  # 1
    start_page = limit * page - 4  # 开始1
    unit2 = Conn.objects.all().values('id')  #总条数
    page_count = math.ceil(len(unit2) / 5)

    conninfo = Conn.objects.all()[start_page-1:start_page+4]
    res_list = []
    for i in conninfo:
        dic = {
            'id': i.id,
            'connname': i.connname,
            'type': i.type,
            'ip': i.ip,
            'port': i.port,
            'username': i.username,
            'databasename': i.databasename,
            'password': i.password,
            'createname': i.createname,
            'createtime': str(i.createtime),
            'editname': i.editname,
            'edittime': str(i.edittime),
            'page_count': page_count,
        }
        password = decrypt_str(dic['password'])
        dic['password'] = password
        res_list.append(dic)

    return res_list









#保存
def saveconn_all(request):
    res = json.loads(request.body)
    cilent = tools.interface_param(request)
    user = cilent.bk_login.get_user({})
    # 通过tools.interface_param获取不到用户名，暂时使用固定名称替代
    res['editname'] = 'zork'
    res['createname'] = 'zork'
    # res['createname'] = user['data']['bk_username']
    # res['editname'] = user['data']['bk_username']
    password = encryption_str(res['password'])
    res['password'] = password
    re = Conn(**res).save()
    return re

#修改
def eidtconnn(request):
    res = json.loads(request.body)
    cilent = tools.interface_param(request)
    user = cilent.bk_login.get_user({})
    # res['editname'] = user['data']['bk_username']
    # 通过tools.interface_param获取不到用户名，暂时使用固定名称替代
    res['editname'] = 'zork'
    res['edittime'] = datetime.datetime.now()

    password = encryption_str(res['password'])
    res['password'] = password
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







