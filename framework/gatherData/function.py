# -*- coding: utf-8 -*-

from models import *
from django.forms.models import model_to_dict
from DataBaseManage.models import *
from DataBaseManage.function import *
import MySQLdb


def gather_data(info):
    gather_type = info['gather_params']
    #采集数据库中的数据
    if "sql" == gather_type:
        conn_info = Conn.objects.filter(id=info['params']).get()
        #解密数据库中的密码
        conn_info.password = decrypt_str(conn_info.password)
        conn = MySQLdb.connect(host=conn_info.ip, user=conn_info.username, passwd=conn_info.password, db=conn_info.databasename, port=int(conn_info.port))
        cursor = conn.cursor()
        result = cursor.execute(info['gather_rule'])
        print result
    elif "interface" == gather_type:
        pass#接口方式采集数据待定
    else:
        pass#文件方式采集数据待定
    return "ok"
