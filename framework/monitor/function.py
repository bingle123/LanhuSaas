# -*- coding: utf-8 -*-
from __future__ import division
from common.log import logger
import json
import math
from models import *
from monitorScene.models import Scene
from DataBaseManage.models import Conn
from DataBaseManage import function
import tools
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.db.models import Q
import pymysql as MySQLdb
import copy


def unit_show(request):

    res = json.loads(request.body)
    limit = res['limit']
    page = res['page']
    unit = Monitor.objects.all()
    p=Paginator(unit, limit)    #分页
    page_count = p.page_range[-1]  #总页数
    page = p.page(page)        #当前页数据
    res_list=[]
    for i in page.object_list:
        j=model_to_dict(i)
        j['page_count']=page_count
        j['edit_time'] = str(i.edit_time)
        j['create_time'] = str(i.create_time)
        j['start_time'] = str (i.start_time)
        j['end_time'] = str (i.end_time)
        res_list.append(j)
    param = {
        'bk_username': 'admin',
        "bk_biz_id": 2,
    }
    client = tools.interface_param (request)
    res = client.job.get_job_list(param)
    if res.get('result'):
        job_list = res.get('data')
    else:
        job_list = []
        logger.error (u"请求作业模板失败：%s" % res.get ('message'))
    job = []
    for i in job_list:
        dic1 = {
            'name':i['name']
        }
        job.append(dic1)
    res_dic = {
        'res_list': res_list,
        'job': job
    }
    result = tools.success_result(res_dic)
    # except Exception as e:
    #     result = tools.error_result(e)
    return result


def select_unit(request):

    res = json.loads(request.body)
    res_list = []
    res1 = "{}".format(res['data'])
    limit = res['limit']
    page = res['page']
    unit =  Monitor.objects.filter(Q(monitor_type__icontains = res1)|Q(monitor_name__icontains = res1)| Q(editor__icontains = res1))
    p = Paginator (unit, limit)  # 分页
    page_count = p.page_range[-1]  # 总页数
    page = p.page (page)  # 当前页数据
    for i in page:
        j = model_to_dict (i)
        j['page_count'] = page_count
        j['edit_time'] = str (i.edit_time)
        j['create_time'] = str (i.create_time)
        j['start_time'] = str (i.start_time)
        j['end_time'] = str (i.end_time)
        res_list.append (j)
    return res_list
    # except Exception as e:
    #     return None


def delete_unit(request):

    try:
        res = json.loads(request.body)
        unit_id = res['unit_id']
        Monitor.objects.filter(id=unit_id).delete()
        if Scene.objects.filter(item_id=unit_id).exists():
            Scene.objects.filter(item_id=unit_id).delete()
        return None
    except Exception as e:
        res1 = tools.error_result(e)
        return res1


def add_unit(request):
    try:
        res = json.loads(request.body)
        cilent = tools.interface_param (request)
        user = cilent.bk_login.get_user({})
        monitor_type = res['monitor_type']
        print(monitor_type)
        if res['monitor_type'] == 'first':
            monitor_type = '基本单元类型'
        if res['monitor_type'] == 'second':
            monitor_type = '图表单元类型'
        if res['monitor_type'] == 'third':
            monitor_type = '作业单元类型'
        if res['monitor_type'] == 'fourth':
            monitor_type = '流程元类型'
        add_dic = res['data']
        add_dic['monitor_name'] = res['monitor_name']
        add_dic['monitor_type'] = monitor_type
        add_dic['jion_id'] = None
        add_dic['status'] = 0
        add_dic['creator'] = user['data']['bk_username']
        add_dic['editor'] = user['data']['bk_username']
        Monitor.objects.create(**add_dic)
        result = tools.success_result(None)
    except Exception as e:
        result = tools.error_result(e)
    return result


def edit_unit(request):
    try:
        res = json.loads (request.body)
        cilent = tools.interface_param (request)
        user = cilent.bk_login.get_user({})
        monitor_type = res['monitor_type']
        print(monitor_type)
        if res['monitor_type'] == 'first':
            monitor_type = '基本单元类型'
        if res['monitor_type'] == 'second':
            monitor_type = '图表单元类型'
        if res['monitor_type'] == 'third':
            monitor_type = '作业单元类型'
        if res['monitor_type'] == 'fourth':
            monitor_type = '流程元类型'
        add_dic = res['data']
        add_dic['monitor_name'] = res['monitor_name']
        add_dic['monitor_type'] = monitor_type
        add_dic['jion_id'] = None
        add_dic['status'] = 0
        add_dic['editor'] = user['data']['bk_username']
        Monitor.objects.filter(monitor_name=res['monitor_name']).update(**add_dic)
        result = tools.success_result(None)
    except Exception as e:
        result = tools.error_result(e)
    return result



def test(request):
    res = json.loads(request.body)
    gather_rule = res['gather_rule']
    server_url = res['server_url']
    sql = Conn.objects.get(id=server_url)
    password = function.decrypt_str(sql.password)
    db = MySQLdb.connect(host=sql.ip, user=sql.username, passwd=password, db=sql.databasename, port=int(sql.port))
    cursor = db.cursor()
    cursor.execute(gather_rule)
    results = cursor.fetchall()
    db.close()
    return results