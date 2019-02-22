# -*- coding: utf-8 -*-
from component.shortcuts import get_client_by_request
from common.log import logger
import base64
from account.models import *
from blueking.component.shortcuts import *
from gatherData.function import gather_data
import time
from monitor.models import Job
from gatherData.function import gather_data_migrate
from gatherData import models
from notification.function import rule_check


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
    click_page_unicode = request.GET.get("clickPage")               # 获取页面页码数
    if click_page_unicode is None or click_page_unicode == "":      # 页码数是否为空，空时赋值为第一页
        click_page = 1
    else:
        click_page = int(click_page_unicode.encode("utf-8"))        # 对页码进行转码
    start_page = (click_page - 1) * limit                           # 接口参数:数据起始页码
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
    return res1

def flow_gather_task(**info):
    task_id=info['task_id']
    item_id=info['item_id']
    node_times=info['node_times']
    client = user_interface_param ()
    param = {
        "bk_biz_id": "2",
        "task_id":task_id
    }
    res = client.sops.get_task_status(param)
    msg=''
    state=res['data']['state']
    temps=res['data']['children']
    keys = temps.keys()
    gather_data_migrate(item_id=item_id)
    if state=='FAILED':
        for key in keys:
            if temps[key]['state']==u'FAILED':
                msg=temps[key]['id']+u'节点执行出错，请检查这个节点'
    elif state=='RUNNING':
        msg=u'该任务正在执行中'
    elif state=='SUSPENDED':
        msg=u'该任务被暂停'
    elif state=='REVOKED':
        msg=u'该任务已被终止'
    elif state=='FINISHED':
        msg=u'该任务成功执行'
    for key in keys:
        models.TDGatherData(item_id=item_id,instance_id=task_id,data_key=key, data_value=temps[key]['state'],gather_error_log=msg).save()
    if item_id!=0:
        rule_check(item_id)