# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
import json
import time
from django.forms.models import model_to_dict
from DataBaseManage.models import *
from framework.shell_app import tools
import MySQLdb
import cx_Oracle
import pymssql
import datetime
from pyDes import *
from binascii import b2a_hex,a2b_hex
import base64
import pyDes

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


#查询所有
def getconn_all(request):
    conninfo = Conn.objects.all()
    res_list = []
    for i in conninfo:
        dic = model_to_dict(i)
        password = decrypt_str(dic['password'])
        dic['password'] = password
        res_list.append(dic)
    return res_list




#保存
def saveconn_all(request):
    res = json.loads(request.body)
    cilent = tools.interface_param(request)
    user = cilent.bk_login.get_user({})
    res['createname'] = user['data']['bk_username']
    res['editname'] = user['data']['bk_username']

    password = encryption_str(res['password'])
    res['password'] = password
    re = Conn(**res).save()
    return re

#修改
def eidtconnn(request):
    res = json.loads(request.body)
    cilent = tools.interface_param(request)
    user = cilent.bk_login.get_user({})
    res['editname'] = user['data']['bk_username']
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







