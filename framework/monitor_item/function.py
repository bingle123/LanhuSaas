# -*- coding: utf-8 -*-
from __future__ import division
from django.db.models import Q
from common.log import logger
import json
import requests
from models import Monitor,Job
from monitor_scene.models import Scene
from db_connection.models import Conn
from monitor_item import tools
from django.forms.models import model_to_dict
import pymysql as MySQLdb
from market_day import function
from market_day import celery_opt as co
from db_connection.function import decrypt_str
from gather_data.function import gather_data, get_db
from gather_data.models import TDGatherData
import sys
from logmanagement.function import add_log, make_log_info, get_active_user
import datetime
from market_day.models import HeaderData as hd
from settings import BK_PAAS_HOST
from django.db import transaction


# 显示函数
def unit_show(request):
    """
    显示函数
    :param request:
    :return:
    """
    # try:
    res = json.loads(request.body)
    #  个数
    limit = res['limit']
    #  当前页面号
    page = res['page']
    unit = Monitor.objects.all()
    # 进入分页函数进行分页，返回总页数和当前页数据
    page_data, base_page_count = tools.page_paging(unit, limit, page)
    #  把返回的数据对象转为list
    res_list = tools.obt_dic(page_data, base_page_count)
    param = {
        'bk_username': 'admin',
        "bk_token": request.COOKIES['bk_token'],
        "bk_biz_id": 2
    }
    param1 = {
        "bk_token": request.COOKIES['bk_token'],
        "bk_biz_id": 2
    }
    #  用user v2的方式调用接口
    client = tools.user_interface_param()
    #  调用获取作业详情接口
    res = client.job.get_job_list(param)
    #  调用获取标准运维模板详情接口
    res1 = client.sops.get_template_list(param1)
    if res.get('result'):
        job_list = res.get('data')
    else:
        job_list = []
        logger.error(u"请求作业模板失败：%s" % res.get('message'))
    if res1.get('result'):
        flow_list = res1.get('data')
    else:
        flow_list = []
        logger.error(u"请求流程模板失败：%s" % res.get('message'))
    job = []
    flow = []
    #  获取模板名称和ID
    for flow_data in flow_list:
        dic2 = {
            'flow_name': flow_data['name'],
            'id': [{
                'name': flow_data['name'],
                'id': flow_data['id']
            }]
        }
        flow.append(dic2)
    for job_data in job_list:
        dic1 = {
            'name': job_data['name'],
            'id': [{
                'name': job_data['name'],
                'id': job_data['bk_job_id']
            }]
        }
        job.append(dic1)
    res_dic = {
        'res_list': res_list,
        'job': job,
        'flow': flow,
    }
    result = tools.success_result(res_dic)
    # except Exception as e:
    #     result = tools.error_result(e)
    return result


# 查询函数
def select_unit(request):
    """
    查询函数
    :param request:
    :return:
    """
    # try:
    res = json.loads(request.body)
    res1 = res['data']
    limit = res['limit']
    page = res['page']
    # 模糊查询
    unit = Monitor.objects.filter(Q(monitor_name__icontains=res1) | Q(editor__icontains=res1))
    page_data, base_page_count = tools.page_paging(unit, limit, page)
    res_list = tools.obt_dic(page_data, base_page_count)
    res_data = tools.success_result(res_list)
    return res_data
    # except Exception as e:
    #     return None


# 删除函数
def delete_unit(request):
    """
    删除函数
    :param request:
    :return:
    """
    try:
        res = json.loads(request.body)
        #  根据前台传的来的id进行删除
        unit_id = res['unit_id']
        monitor_name = res['monitor_name']
        Monitor.objects.filter(id=unit_id).delete()
        co.delete_task(unit_id)
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
    """
    新增监控项（1：基本监控项，2：图表监控项，3：作业监控兴，4：流程监控项）
    :param request:页面请求对象
    :return:result
    """
    try:
        # 添加事物控制防止异常时事物不回滚，这里事物必须放在try...catch里面
        # 否则事物被try...catch捕获了就不起作用了
        with transaction.atomic():
            # 修改获取用户的方式，直接从request中获取
            username = request.user.username
            res = json.loads(request.body)
            add_dic = res['data']
            print add_dic
            add_flow_dic = res['flow']
            monitor_type = res['monitor_type']
            #  根据前台来的单元类型进行分类
            if res['monitor_type'] == 'first':
                monitor_type = 1
            if res['monitor_type'] == 'second':
                monitor_type = 2
            if res['monitor_type'] == 'third':
                monitor_type = 3
                #  作业监控项的把作业id和name分别存放
                add_dic['jion_id'] = res['data']['gather_rule'][0]['id']
                add_dic['gather_rule'] = res['data']['gather_rule'][0]['name']
            if res['monitor_type'] == 'fourth':
                monitor_type = 4
                add_dic['jion_id'] = res['flow']['jion_id']
                add_dic['gather_params'] = add_dic['node_name']
                add_dic.pop('node_name')
                add_dic['gather_rule'] = res['data']['gather_rule'][0]['name']
                add_dic['params'] = res['flow']['constants']
                add_flow_dic['monitor_area']=res['monitor_area']
                start_list = []
                for i in res['flow']['node_times']:
                    start_list.append(i['endtime'])
                    start_list.append(i['starttime'])
                add_dic['start_time'] = min(start_list)
                add_dic['end_time'] = max(start_list)
                add_flow_dic['start_time']=add_dic['start_time']
                add_flow_dic['end_time'] =add_dic['end_time']
                print add_flow_dic
            add_dic['monitor_name'] = res['monitor_name']
            # 新增一条数据时 开关状态默认为0 关闭
            add_dic['status'] = 0
            add_dic['monitor_type'] = monitor_type
            add_dic['creator'] = username
            add_dic['editor'] = username
            add_dic['monitor_area'] = res['monitor_area']
            Monitor.objects.create(**add_dic)
            # 添加定时任务监控要求本地安装任务调度软件rabitmq
            # 正式环境服务器一般带有这个调度软件，如果没有就要安装
            if res['monitor_type'] == 'fourth':
                function.add_unit_task(add_dicx=add_flow_dic)
            else:
                function.add_unit_task(add_dicx=add_dic)
            result = tools.success_result(None)
            # 修改获取用户的方式，直接从request中获取
            info = make_log_info(u'增加监控项', u'业务日志', u'Monitor', sys._getframe().f_code.co_name,
                                 request.user.username, '成功', '无')
    except Exception as e:
        info = make_log_info(u'增加监控项', u'业务日志', u'Monitor', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
        result = tools.error_result(e)
    add_log(info)
    return result


def edit_unit(request):

    """
    修改监控项（1：基本监控项，2：图表监控项，3：作业监控兴，4：流程监控项）
    :param request: 页面请求对象
    :return: result
    """
    try:
        # 添加事物控制防止异常时事物不回滚，这里事物必须放在try...catch里面
        # 否则事物被try...catch捕获了就不起作用了
        with transaction.atomic():
            res = json.loads(request.body)
            id = res['unit_id']
            # 修改获取用户的方式，直接从request中获取
            username = request.user.username
            monitor_type = res['monitor_type']
            # 把前台来的监控项数据一次性转为字典
            add_dic = res['data']
            if res['monitor_type'] == 'first':
                monitor_type = '1'
            if res['monitor_type'] == 'second':
                monitor_type = '2'
            if res['monitor_type'] == 'third':
                monitor_type = '3'
                # id和name要拆分
                add_dic['jion_id'] = res['data']['gather_rule'][0]['id']
                add_dic['gather_rule'] = res['data']['gather_rule'][0]['name']
            if res['monitor_type'] == 'fourth':
                monitor_type = '4'
                # 前台来的id和name要拆分
                add_dic['jion_id'] = res['flow']['jion_id']
                add_dic['gather_params'] = add_dic['node_name']
                add_dic['gather_rule'] = res['data']['gather_rule'][0]['name']
                node_times = res['flow']['node_times']
                constants = res['flow']['constants']
                add_dic.pop('node_name')
                start_list = []
                for data in res['flow']['node_times']:
                    start_list.append(data['endtime'])
                    start_list.append(data['starttime'])
                add_dic['start_time'] = min(start_list)
                add_dic['end_time'] = max(start_list)
            add_dic['monitor_name'] = res['monitor_name']
            add_dic['monitor_type'] = monitor_type
            # 当前用户为编辑人
            add_dic['editor'] = username
            add_dic['monitor_area'] = res['monitor_area']
            Monitor.objects.filter(id=id).update(**add_dic)
            if res['monitor_type'] == 'fourth':
                add_dic['node_times'] = node_times
                add_dic['constants'] = constants
                add_dic['monitor_type']='fourth'
            # 添加定时任务监控要求本地安装任务调度软件rabitmq
            # 正式环境服务器一般带有这个调度软件，如果没有就要安装
            function.add_unit_task(add_dicx=add_dic)
            result = tools.success_result(None)
            # 修改获取用户的方式，直接从request中获取
            info = make_log_info(u'编辑监控项', u'业务日志', u'Monitor', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
    except Exception as e:
        info = make_log_info(u'编辑监控项', u'业务日志', u'Monitor', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
        result = tools.error_result(e)
        add_log(info)
    return result


# 基本监控项采集测试
def basic_test(request):
    """
    基本监控项采集测试
    :param request:
    :return:
    """
    info = json.loads(request.body)
    # 新增时测试
    if info['id'] == '':
        info['id'] = 0
    result = []
    gather_data(**info)
    gather_rule2 = "select data_key,data_value,gather_error_log from td_gather_data where item_id = " + str(info['id'])
    # 获得数据库对象
    db = get_db()
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


# 作业采集测试
def job_test(request):
    res = json.loads(request.body)
    # 采集测试id为0 用于与队列调度区分
    res['id'] = 0
    result = tools.job_interface(res)
    return result


# 改变监控项的启用状态
def change_unit_status(req):
    """
    改变监控项的启用状态
    :param req:
    :return:
    """
    try:
        res = json.loads(req.body)
        flag = int(res['flag'])
        unit_id = res['id']
        schename = str(unit_id)
        mon = Monitor.objects.get(id=unit_id)
        mon.status = flag
        mon.save()
        if flag == 1:
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
    # 测试数据
    database_id = request_body['database_id']

    info = {}
    info['id'] = '71'  # id采集测试用的随意值
    info['gather_params'] = 'sql'  # 图表监控项是sql语句查询
    info['params'] = request_body['database_id']
    info['gather_rule'] = request_body['sql']
    sql = request_body['sql']
    # 调用gatherData方法
    gather_data(**info)
    # sql查询列的名称
    column_name_temp = sql.split('@')
    column_name_list = []
    execute_sql = ''
    # 列名称和执行的sql
    for i in range(0, len(column_name_temp)):
        if i == 0 or i == len(column_name_temp) - 1:
            execute_sql += column_name_temp[i]
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
    """

    :param request:
    :param id:
    :return:
    """
    cookies = request.COOKIES
    a_url = BK_PAAS_HOST + "/o/bk_sops/api/v3/template/{}/".format(id[0]['id'])
    req = requests.get(url=a_url, cookies=cookies)
    req.encoding = req.apparent_encoding
    req.raise_for_status()
    return json.loads(req.text)


def get_flow_desc(request):
    """

    :param request:
    :return:
    """
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
    """

    :param request:
    :return:
    """
    cilent = tools.interface_param(request)
    id = json.loads(request.body)
    activities2 = []
    res = get_desc(request, id['template_id'])
    res1 = json.loads(res['pipeline_tree'])
    location = res1['location']
    gateways = res1['gateways']
    for i in gateways:
        gateways1 = {}
        gateways1['type'] = gateways[i]['type']
        gateways1['id'] = gateways[i]['id']
        gateways1['name'] = gateways[i]['name']
        gateways1['outgoing'] = gateways[i]['outgoing']
        gateways1['incoming'] = gateways[i]['incoming']
        for f in location:
            if f['id'] == gateways[i]['id']:
                gateways1['x'] = f['x']
                gateways1['y'] = f['y']
                activities2.append(gateways1)
    start_event = res1['start_event']  # 开始节点信息
    for l in location:
        if l['id'] == start_event['id']:
            start_event['x'] = l['x']
            start_event['y'] = l['y']
    end_event = res1['end_event']  # 结束节点信息
    for l in location:
        if l['id'] == end_event['id']:
            end_event['x'] = l['x']
            end_event['y'] = l['y']

    activities2.append(start_event)
    activities2.append(end_event)
    activities = res1['activities']
    for key in activities:
        activities1 = {}
        activities1['id'] = str(activities[key]['id'])
        activities1['type'] = str(activities[key]['type'])
        activities1['name'] = activities[key]['name']
        activities1['stage_name'] = activities[key]['stage_name']
        for l in location:
            if l['id'] == activities1['id']:
                activities1['x'] = l['x']
                activities1['y'] = l['y']
                activities2.append(activities1)
    flows1 = []
    flows2 = res1['flows']
    for i in res1['line']:
        flows3 = {
            'source': {
                'arrow': i['source']['arrow'],
                'id': i['source']['id']
            },
            'target': {
                'arrow': i['target']['arrow'],
                'id': i['target']['id']
            }
        }
        flows1.append(flows3)
    constants1 = []
    constants = res1['constants']
    for key in constants:
        constants2 = {}
        constants2['name'] = constants[key]["name"]
        constants2['value'] = constants[key]["value"]
        constants2['key'] = constants[key]["key"]
        constants1.append(constants2)
    pipeline_tree = {
        'activities': activities2,
        'flows': flows1,
        'constants': constants1,
        'template_id': id['template_id']
    }
    return pipeline_tree


def node_name(request):
    """

    :param request:
    :return:
    """
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
    """

    :param request:
    :return:
    """
    res = json.loads(request.body)
    item_id = res['item_id']['message']
    print item_id
    data = TDGatherData.objects.filter(instance_id=item_id)
    data1 = []
    for i in data:
        dic = {

            'data_key': i.data_key,
            'data_value': i.data_value
        }
        data1.append(dic)
    return data1


def node_state_by_item_id(request):
    """

    :param request:
    :return:
    """
    res = json.loads(request.body)
    item_id = res['item_id']
    print item_id
    data = TDGatherData.objects.filter(item_id=item_id)
    data1 = []
    for i in data:
        dic = {

            'data_key': i.data_key,
            'data_value': i.data_value
        }
        data1.append(dic)
    return data1
