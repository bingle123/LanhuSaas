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
import pymssql
import copy
import base64
import re
from market_day import function
from market_day import celery_opt as co
from DataBaseManage.function import decrypt_str


def unit_show(request):
    try:
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
        param1 = {
            "bk_biz_id": 2,
        }
        client = tools.interface_param (request)
        res = client.job.get_job_list(param)
        res1 = client.sops.get_template_list(param1)
        if res.get('result'):
            job_list = res.get('data')
        else:
            job_list = []
            logger.error (u"请求作业模板失败：%s" % res.get ('message'))
        if res1.get ('result'):
            flow_list = res1.get ('data')
        else:
            flow_list = []
            logger.error (u"请求流程模板失败：%s" % res.get ('message'))
        job = []
        flow = []
        for i in flow_list:
            dic2 = {
                'flow_name': i['name'],
                'id': i['bk_biz_id']
            }
            flow.append(dic2)
        for i in job_list:
            dic1 = {
                'name': i['name'],
                'id': i['bk_job_id']
            }
            job.append(dic1)
        res_dic = {
            'res_list': res_list,
            'job': job,
            'flow': flow,
        }
        result = tools.success_result(res_dic)
    except Exception as e:
        result = tools.error_result(e)
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
        schename=res['monitor_name']
        Monitor.objects.filter(id=unit_id).delete()
        co.delete_task(schename)
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
        print add_dic['params']
        print add_dic
        Monitor.objects.create(**add_dic)
        function.add_unit_task(add_dicx=add_dic)
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
        function.edit_unit_task(add_dicx=add_dic)
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
    if sql.type == 'MySQL' or sql.type == 'Oracle':
        db = MySQLdb.connect(host=sql.ip, user=sql.username, passwd=password, db=sql.databasename, port=int(sql.port))
    if sql.type == 'SQL Server':
        db = pymssql.connect(sql.ip, sql.username, password, sql.databasename)
    cursor = db.cursor()
    cursor.execute(gather_rule)
    results = cursor.fetchall()
    db.close()
    return results


def job_test(request):
    try:
        res = json.loads(request.body)
        x = res['params']
        x1 = x.decode('utf-8')
        bk_job_id = res['job_id']
        script_param = base64.b64encode(x1)
        cilent = tools.interface_param(request)
        select_job_params = {
            'bk_biz_id': 2,
            'bk_job_id': bk_job_id,
        }
        select_job = cilent.job.get_job_detail(select_job_params)
        if select_job.get('result'):
            select_job_list = select_job.get('data')
        else:
            select_job_list = []
            logger.error(u"请求作业模板失败：%s" % select_job.get('message'))
        step_id = select_job_list['steps'][0]['step_id']

        job_params = {
            'bk_biz_id': 2,
            'bk_job_id': bk_job_id,
            'steps': [{
                'step_id': step_id,
                'script_param': script_param
            }]
        }
        job = cilent.job.execute_job(job_params)
        if job.get('result'):
            job_list = job.get('data')
        else:
            job_list = []
            logger.error(u"请求作业模板失败：%s" % job.get('message'))
        res = tools.success_result(job_list)
    except Exception as e:
        res = tools.error_result(e)
    return res


def change_unit_status(req):
    res=json.loads(req.body)
    schename=res['monitor_name']
    flag=res['flag']
    unit_id=res['id']
    mon=Monitor.objects.get(id=unit_id)
    mon.status=flag
    mon.save()
    if flag==0:
        co.enable_task(schename)
    else:
        co.disable_task(schename)
    return tools.success_result(None)


def chart_get_test(request):
    """
    图表单元采集测试
    :param request:
    :return:
    """
    request_body = json.loads(request.body)
    database_id = request_body['database_id']
    sql = request_body['sql']

    # 假定数据
    # database_id = 4
    # sql = 'SELECT count(*)@人口数@,cityName@城市名称@ from city GROUP BY cityName'

    # sql查询列的名称
    column_name_temp = sql.split('@')
    column_name_list = []
    execute_sql = ''
    # 列名称和执行的sql
    for i in range(0, len(column_name_temp)):
        if i % 2 == 1:
            column_name_list.append(column_name_temp[i])
        else:
            execute_sql += column_name_temp[i]
    print execute_sql
    # 更具数据库ID查询数据库配置
    database_result = list(Conn.objects.filter(id=database_id).values())
    # 数据库参数
    username = database_result[0]['username']
    database = database_result[0]['databasename']
    password = decrypt_str(database_result[0]['password'])
    host = database_result[0]['ip']
    port = str(database_result[0]['port'])
    db = MySQLdb.connect(host=host, user=username, passwd=password, db=database, port=int(port), charset='utf8')
    cursor = db.cursor()
    cursor.execute(execute_sql)
    results = cursor.fetchall()
    db.close()
    result_list = []
    for i in results:
        temp_dict = {}
        temp_dict['value'] = list(i)[1].encode('utf-8')
        temp_dict['name'] = list(i)[0]
        result_list.append(temp_dict)
    return {
        "result": True,
        "message": u'成功',
        "code": 0,
        "results": result_list,
        "column_name_list": column_name_list,
    }
