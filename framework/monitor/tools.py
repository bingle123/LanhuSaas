# -*- coding: utf-8 -*-
from blueking.component.shortcuts import get_client_by_request
from common.log import logger
import base64
from account.models import *
from blueking.component.shortcuts import *
from gatherData.function import gather_data
from datetime import datetime
import time
from monitor.models import Job
from gatherData.function import gather_data_migrate
from gatherData import models
from notification.function import rule_check
from market_day import celery_opt as co
from djcelery import models as celery_models
from models import *


def error_result(e):
    """
    失败统一JSON
    :param e:   异常
    :return:    json数据
    """
    result = {
        "result": False,
        "message": u"失败 %s" % e,
        "code": 1,
        "results": None
    }
    return result


def success_result(results):
    """
    成功统一JSON
    :param results:
    :return:
    """
    result = {
        "result": True,
        "message": u'成功',
        "code": 0,
        "results": results,
    }
    return result


def page_paging(request, limit):
    """
    分页方法
    :param request:
    :param limit:   页面容量
    :return:        页面起始页码
    """
    click_page_unicode = request.GET.get("clickPage")  # 获取页面页码数
    if click_page_unicode is None or click_page_unicode == "":  # 页码数是否为空，空时赋值为第一页
        click_page = 1
    else:
        click_page = int(click_page_unicode.encode("utf-8"))  # 对页码进行转码
    start_page = (click_page - 1) * limit  # 接口参数:数据起始页码
    return start_page


def interface_param(request):
    """
    返回client对象
    :param request:
    :return:
    """
    client = get_client_by_request(request)                         # 获取code、secret参数
    client.set_bk_api_ver('v2')                                     # 以v2版本调用接口
    return client


def user_interface_param():
    """
    返回client对象
    :param :
    :return:
    """
    user_account = BkUser.objects.filter (id=1).get ()
    client = get_client_by_user (user_account)
    client.set_bk_api_ver ('v2')                                    # 以v2版本调用接口
    return client

def job_interface(res):
    try:
        params = res['params']  # ip
        gather_params = res['gather_params']
        bk_job_id = res['job_id'][0]['id']
        script_param = base64.b64encode (gather_params)
        # 根据id为1的用户获取客户端操作快速执行脚本
        client = user_interface_param()
        select_job_params = {
            'bk_biz_id': 2,
            'bk_job_id': bk_job_id,
        }
        select_job = client.job.get_job_detail (select_job_params)
        if select_job.get ('result'):
            select_job_list = select_job.get ('data')
        else:
            select_job_list = []
            logger.error (u"请求作业模板失败：%s" % select_job.get ('message'))
        step_id = select_job_list['steps'][0]['step_id']
        cloud_params = {
            'bk_biz_id': 2,
            'ip': {
                'data': [params,],
                'exact': 1
            },
            "condition": [
                {
                    "bk_obj_id": "host",
                    "fields": [],
                    "condition": [
                        {
                            "field": "bk_host_innerip",
                            "operator": "$eq",
                            "value": params
                        }
                    ]
                }]
        }
        cloud_select = client.cc.search_host (cloud_params)
        if cloud_select.get ('result'):
            cloud_id = cloud_select['data']['info'][0]['host']['bk_cloud_id'][0]['id']
        else:
            cloud_id = -1
            logger.error (u"请求主机信息失败：%s" % cloud_select.get ('message'))
        job_params = {
            'bk_biz_id': 2,
            'bk_job_id': bk_job_id,
            'steps': [{
                'step_id': step_id,
                'script_param': script_param,
                "ip_list": [{
                    "bk_cloud_id": cloud_id,
                    "ip": params
                }, ]
            }, ],
        }
        job = client.job.execute_job(job_params)
        if job.get ('result'):
            job_list = job.get ('data')
            job_instance_id = job_list['job_instance_id']
        else:
            job_list = []
            job_instance_id = 0
            logger.error (u"请求作业模板失败：%s" % job.get ('message'))
        log_params = {
            "bk_biz_id": "2",
            "job_instance_id": job_instance_id
        }
        log = client.job.get_job_instance_log(log_params)
        while 'True' != str (log['data'][0]['is_finished']):
            time.sleep(3)
            log = client.job.get_job_instance_log(log_params)
        json_data = log['data'][0]['step_results'][0]['ip_logs'][0]['log_content']
        if log['data'][0]['status'] ==3:
            status=1
        else:
            status = -2
        res1 = success_result(job_list)
    except Exception as e:
        res1 = error_result(e)
        status = -1
    try:
        name_status  = job['data']['job_instance_name']
        info = {
            'id': res['id'],                       # 关联id
            'data_key': name_status,               # 状态key
            'gather_params': 'space_interface',  # 类型
            'data_value':status,                   #状态value
            'gather_error_log': {                 #采集数据
                'data_key':json_data
            } ,
            'instance_id': job_list['job_instance_id']     #实列id
        }
        gather_data (info)
        if res['id']==0:
            Job(instance_id=job_instance_id,status=status,test_flag=0,job_log=info['gather_error_log'],job_id=bk_job_id).save()
        else:
            Job (instance_id=job_instance_id, status=status, test_flag=1,job_log=info['gather_error_log'],job_id=bk_job_id).save()
    except Exception as e:
        res1 = error_result(e)
    return res1

def flow_gather_task(**info):
    task_id = info['task_id']
    item_id = info['item_id']
    node_times = info['node_times']
    user_account = BkUser.objects.filter(id=1).get()
    # 根据id为1的用户获取客户端操作快速执行脚本
    client = get_client_by_user(user_account)
    client.set_bk_api_ver('v2')
    param = {
        "bk_biz_id": "2",
        "task_id": task_id
    }
    res = client.sops.get_task_status(param)
    msg = ''
    state = res['data']['state']
    temps = res['data']['children']
    keys = temps.keys()
    flag=info['flag']
    task_name=info['task_name']
    gather_data_migrate(item_id=item_id)
    status=0
    if state == 'FAILED':
        status = 1
        if flag:
            co.delete_task(task_name)
        for key in keys:
            if temps[key]['state'] == u'FAILED':
                msg = temps[key]['id'] + u'节点执行出错，请检查这个节点'
    elif state == 'RUNNING':
        status = 2
        msg = u'该任务正在执行中'
    elif state == 'SUSPENDED':
        status = 3
        msg = u'该任务被暂停'
    elif state == 'REVOKED':
        status = 4
        msg = u'该任务已被终止'
        if flag:
            co.delete_task(task_name)
    elif state == 'FINISHED':
        status = 5
        msg = u'该任务成功执行'
        if flag:
            co.delete_task(task_name)
    for key in keys:
        models.TDGatherData(item_id=item_id, instance_id=task_id, data_key=key, data_value=temps[key]['state'],
                            gather_error_log=msg).save()
    if item_id != 0:
        rule_check(item_id)

def start_flow_task(**info):
    # 得到client对象，方便调用接口
    user_account = BkUser.objects.filter(id=1).get()
    client = get_client_by_user(user_account)
    client.set_bk_api_ver('v2')
    template_id = info['template_list']['id']
    constants_temp = info['constants']
    constants={}
    for temp in constants_temp:
        constants[temp['key']]=temp['value']
    strnow = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    name = info['template_list']['name'] + strnow
    param = {
        "bk_biz_id": "2",
        "template_id": template_id,
        'name': name,
        'constants': constants
    }
    res = client.sops.create_task(param)
    # 调用接口创建任务并得到任务的id
    task_id = res['data']['task_id']
    # 调用接口启动任务，开始执行任务
    param = {
        "bk_biz_id": "2",
        'task_id': task_id
    }
    res = client.sops.start_task(param)
    flag = res['result']
    status=0
    # 如果启动任务成功创建一个定时查看节点状态的任务
    if flag:
        node_times = info['node_times']
        starthour = str(node_times[-1]['starttime']).split(':')[0]
        endhour = str(node_times[0]['endtime'])[:2].split(':')[0]
        period = info['period']
        item_id=0
        args = {
            'item_id': item_id,
            'task_id': task_id,  # 启动流程的任务id
            'node_times': node_times,
            'period': period,
            'flag':True,
            'task_name':info['template_list']['name'] + '_check_status_test'
        }
        ctime = {
            'every': period,
            'period': 'seconds'
        }
        co.create_task_interval(name=info['template_list']['name'] + '_check_status_test',
                               task='market_day.tasks.gather_data_task_thrid', interval_time=ctime,
                               task_args=args, desc=name)
        status=1
        for time in node_times:
            Flow_Node(flow_id=item_id,node_name=time['node_name'],start_time=time['starttime'], end_time=time['endtime']).save()
    Flow(instance_id=task_id, status=flag, test_flag=1, flow_id=item_id).save()
    return task_id

