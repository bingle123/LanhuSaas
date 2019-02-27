# -*- coding: utf-8 -*-
from __future__ import division
from django.db.models import Q
from common.log import logger
import json
import requests
from models import Monitor
from monitorScene.models import Scene
from db_connection.models import Conn
from monitor import tools
from django.forms.models import model_to_dict
import pymysql as MySQLdb
from market_day import function
from market_day import celery_opt as co
from db_connection.function import decrypt_str
from gatherData.function import gather_data,get_db
from gatherData.models import TDGatherData
import sys
from logmanagement.function import add_log,make_log_info,get_active_user
import datetime


def unit_show(request):
    try:
        res = json.loads(request.body)
        limit = res['limit']
        page = res['page']
        unit = Monitor.objects.all()
        page_data, base_page_count = tools.page_paging(unit,limit,page)
        res_list= tools.obt_dic(page_data,base_page_count)
        param = {
            'bk_username': 'admin',
            "bk_biz_id": 2,
        }
        param1 = {
            "bk_biz_id": 2,
        }
        client = tools.user_interface_param()
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
                'id': [{
                    'name': i['name'],
                    'id': i['id']
                }]
            }
            flow.append(dic2)
        for i in job_list:
            dic1 = {
                'name': i['name'],
                'id': [{
                    'name': i['name'],
                    'id': i['bk_job_id']
                }]
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
    try:
        res = json.loads(request.body)
        res_list = []
        res1 = res['data']
        limit = res['limit']
        page = res['page']
        unit =  Monitor.objects.filter(Q(monitor_type__icontains = res1)|Q(monitor_name__icontains = res1)| Q(editor__icontains = res1))
        page_data, base_page_count = tools.page_paging(unit,limit,page)
        res_list= tools.obt_dic(page_data,base_page_count)
        return res_list
    except Exception as e:
        return None


def delete_unit(request):
    try:
        res = json.loads(request.body)
        unit_id = res['unit_id']
        monitor_name=res['monitor_name']
        Monitor.objects.filter(id=unit_id).delete()
        co.delete_task(monitor_name)
        res1 = tools.success_result(None)
        info = make_log_info(u'删除监控项', u'业务日志', u'Monitor', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'删除监控项', u'业务日志', u'Monitor', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '失败', repr(e))
        res1 = tools.error_result(e)
    add_log(info)
    return res1


def add_unit(request):
    try:
        res = json.loads(request.body)
        cilent = tools.interface_param (request)
        user = cilent.bk_login.get_user({})
        add_dic = res['data']
        add_flow_dic = res['flow']
        monitor_type = res['monitor_type']
        if res['monitor_type'] == 'first':
            monitor_type = '基本单元类型'
        if res['monitor_type'] == 'second':
            monitor_type = '图表单元类型'
        if res['monitor_type'] == 'third':
            monitor_type = '作业单元类型'
            add_dic['jion_id'] = res['data']['gather_rule'][0]['id']
            add_dic['gather_rule'] = res['data']['gather_rule'][0]['name']
        if res['monitor_type'] == 'fourth':
            monitor_type = '流程单元类型'
            add_dic['jion_id'] = res['flow']['jion_id']
            add_dic['gather_params'] = add_dic['node_name']
            add_dic.pop('node_name')
            add_dic['gather_rule'] = res['data']['gather_rule'][0]['name']
            add_dic['params']=res['flow']['constants']
            start_list = []
            for i in res['flow']['node_times']:
                start_list.append(i['endtime'])
                start_list.append(i['starttime'])
            add_dic['start_time']=min(start_list)
            add_dic['end_time'] =max(start_list)
        add_dic['monitor_name'] = res['monitor_name']
        add_dic['status'] = 0
        add_dic['monitor_type'] = monitor_type
        add_dic['creator'] = user['data']['bk_username']
        add_dic['editor'] = user['data']['bk_username']
        Monitor.objects.create(**add_dic)
        if res['monitor_type'] == 'fourth':
            function.add_unit_task(add_dicx=add_flow_dic)
        else:
            function.add_unit_task(add_dicx=add_dic)
        result = tools.success_result(None)
        info = make_log_info(u'增加监控项', u'业务日志', u'Monitor', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'增加监控项', u'业务日志', u'Monitor', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '失败', repr(e))
        result = tools.error_result(e)
    add_log(info)
    return result


def edit_unit(request):
    try:
        res = json.loads (request.body)
        id = res['unit_id']
        cilent = tools.interface_param (request)
        user = cilent.bk_login.get_user({})
        monitor_type = res['monitor_type']
        add_dic = res['data']
        if res['monitor_type'] == 'first':
            monitor_type = '基本单元类型'
        if res['monitor_type'] == 'second':
            monitor_type = '图表单元类型'
        if res['monitor_type'] == 'third':
            monitor_type = '作业单元类型'
        if res['monitor_type'] == 'fourth':
            monitor_type = '流程单元类型'
            add_dic['jion_id'] = res['flow']['jion_id']
            add_dic['gather_params'] = add_dic['node_name']
            add_dic['gather_rule'] = res['data']['gather_rule'][0]['name']
            add_dic.pop('node_name')
            start_list = []
            for i in res['flow']['node_times']:
                start_list.append(i['endtime'])
                start_list.append(i['starttime'])
            add_dic['start_time']=min(start_list)
            add_dic['end_time'] =max(start_list)
        add_dic['monitor_name'] = res['monitor_name']
        add_dic['monitor_type'] = monitor_type
        add_dic['editor'] = user['data']['bk_username']
        Monitor.objects.filter(id=id).update(**add_dic)
        function.add_unit_task(add_dicx=add_dic)
        result = tools.success_result(None)
        info = make_log_info(u'编辑监控项', u'业务日志', u'Monitor', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'编辑监控项', u'业务日志', u'Monitor', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '失败', repr(e))
        result = tools.error_result(e)
    add_log(info)
    return result


def basic_test(request):
    info = json.loads(request.body)
    result = []
    gather_data(info)
    gather_rule2 = "select data_key,data_value,gather_error_log from td_gather_data where item_id = " + str(info['id'])
    db = get_db(info['params'])
    cursor = db.cursor()
    cursor.execute(gather_rule2)
    results = cursor.fetchall()
    dic = {}
    for i in results:
        dic1 = {
            i[0]: i[1],
            'gather_status': i[2]
        }
        dic = dict(dic, **dic1)
    result.append(dic)
    db.close()
    return result


def job_test(request):

    res = json.loads(request.body)
    res['id'] = 0
    result = tools.job_interface(res)
    return result


def change_unit_status(req):
    try:
        res=json.loads(req.body)
        flag=int(res['flag'])
        unit_id=res['id']
        schename=str(unit_id)
        mon=Monitor.objects.get(id=unit_id)
        mon.status=flag
        mon.save()
        if flag==1:
            co.enable_task(schename)
        else:
            co.disable_task(schename)
        res = tools.success_result(None)
    except Exception as e:
        res = tools.error_result(e)
    return res


def chart_get_test(request):
    """
    图表单元采集测试
    :param request:
    :return:
    """
    request_body = json.loads(request.body)
    #测试数据
    database_id=request_body['database_id']

    info={}
    info['id'] = '71' #id测试用的随意值
    info['gather_params'] = 'sql' #图表监控项是sql语句查询
    info['params'] = request_body['database_id']
    info['gather_rule']=request_body['sql']
    sql = request_body['sql']
    #调用gatherData方法
    gather_data(info)
    # sql查询列的名称
    column_name_temp = sql.split('@')
    column_name_list = []
    execute_sql = ''
    # 列名称和执行的sql
    for i in range(0, len(column_name_temp)):
        if i==0 or i==len(column_name_temp)-1:
            execute_sql+=column_name_temp[i]
        else:
            print column_name_temp[i].split('=')
            execute_sql += (column_name_temp[i].split('=')[-1])
            column_name_list.append(column_name_temp[i].split('=')[0])
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
        temp_dict['name'] = list(i)[1].encode('utf-8')
        temp_dict['value'] = list(i)[0]
        result_list.append(temp_dict)
    return {
        "result": True,
        "message": u'成功',
        "code": 0,
        "results": result_list,
        "column_name_list": column_name_list,
    }

def get_desc(request, id):
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Cookie': 'csrftoken=bNAyZ7pBsJ1OEi8TMq1NqxNXY2CUREEO; sessionid=r9g2ofn1wb0ykd1epg8crk9l5pgyeuu2; bk_csrftoken=GdxslZh1U3YVsCthqXIv09PbVoW0AaQd; bklogin_csrftoken=z8goJXIMXil80lFT3VtLQHMClrPIExl9; blueking_language=zh-cn; bk_token=kxgoYlRp77AkbGVX85AdFVR0t6eqqHeJ-BlMXxA6oM0',
        'Host': 'paas.bk.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3679.0 Safari/537.36',
        'X-CSRFToken': 'FI1fszvZzgIsYYX8n6aPMduEeAL7qTV3',
        'X-Requested-With': 'XMLHttpRequest'
    }
    csrftoken = request.COOKIES["csrftoken"];
    Cookie="keyA=1";
    for key in request.COOKIES:
        Cookie = "%s;%s=%s"%(Cookie,key,request.COOKIES[key]);
    headers['Cookie'] = Cookie;
    headers['X-CSRFToken'] = csrftoken;
    a_url="http://paas.bk.com/o/bk_sops/api/v3/template/{}/".format(id[0]['id']);
    req=requests.get(url=a_url,headers=headers)
    req.encoding=req.apparent_encoding
    req.raise_for_status()
    return json.loads(req.text)

def get_flow_desc(request):
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Cookie': 'csrftoken=bNAyZ7pBsJ1OEi8TMq1NqxNXY2CUREEO; sessionid=r9g2ofn1wb0ykd1epg8crk9l5pgyeuu2; bk_csrftoken=GdxslZh1U3YVsCthqXIv09PbVoW0AaQd; bklogin_csrftoken=z8goJXIMXil80lFT3VtLQHMClrPIExl9; blueking_language=zh-cn; bk_token=kxgoYlRp77AkbGVX85AdFVR0t6eqqHeJ-BlMXxA6oM0',
        'Host': 'paas.bk.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3679.0 Safari/537.36',
        'X-CSRFToken': 'FI1fszvZzgIsYYX8n6aPMduEeAL7qTV3',
        'X-Requested-With': 'XMLHttpRequest'
    }
    csrftoken = request.COOKIES["csrftoken"];
    Cookie = "keyA=1";
    for key in request.COOKIES:
        Cookie = "%s;%s=%s" % (Cookie, key, request.COOKIES[key]);
    headers['Cookie'] = Cookie;
    headers['X-CSRFToken'] = csrftoken;
def flow_change(request):

    cilent = tools.interface_param (request)
    id = json.loads(request.body)
    res = get_desc(request, id['template_id'])
    res1=json.loads(res['pipeline_tree'])
    activities2 = []
    start_event = res1['start_event']  #开始节点信息
    location = res1['location']
    for l in location:
        if l['id']==start_event['id']:
            start_event['x'] = l['x']*0.5
            start_event['y'] = l['y']
    end_event = res1['end_event']   #结束节点信息
    for l in location:
        if l['id']==end_event['id']:
            end_event['x'] = l['x']*0.5
            end_event['y'] = l['y']

    activities2.append(start_event)
    activities2.append(end_event)
    activities = res1['activities']
    for key in activities:
        activities1 = {}
        activities1['id'] = str(activities[key]['id'])
        activities1['type'] = str(activities[key]['type'])
        activities1['name'] = activities[key]['name']
        for l in location:
            if l['id']==activities1['id']:
                activities1['x'] = l['x']*0.5
                activities1['y'] = l['y']
                activities2.append(activities1)
    flows1=[]
    flows2 = res1['flows']
    for key in flows2:
        flows3 = {
            'source':{
                'arrow': 'Right',
                'id':str(flows2[key]['source'])
            },
            'target':{
                'arrow':'Left',
                'id':str(flows2[key]['target'])
            }
        }
        # flows3['source'] = str(flows2[key]['source'])
        # flows3['target'] = str(flows2[key]['target'])
        flows1.append(flows3)
    constants1= []
    constants = res1['constants']
    for key in constants:
        constants2={}
        constants2['name']=constants[key]["name"]
        constants2['value']=constants[key]["value"]
        constants2['key']=constants[key]["key"]
        constants1.append(constants2)
    pipeline_tree={
        'activities':activities2,
        'flows':flows1,
        'constants':constants1,
        'template_id':id['template_id']
    }
    return pipeline_tree

def node_name(request):
    id = json.loads(request.body)
    res = get_desc(request, id['id'])
    res1 = json.loads(res['pipeline_tree'])
    activities2 = []
    location = res1['location']
    activities = res1['activities']
    for key in activities:
        activities1 = {}
        activities1['name'] = activities[key]['name']
        activities2.append(activities1)
    pipeline_tree = {
        'activities': activities2
    }
    return pipeline_tree

def node_state(request):
    res = json.loads(request.body)
    item_id= res['item_id']['message']
    print item_id
    data = TDGatherData.objects.filter(instance_id=item_id)
    data1=[]
    for i in data:
        dic={

            'data_key':i.data_key,
            'data_value':i.data_value
        }
        data1.append(dic)
    return data1