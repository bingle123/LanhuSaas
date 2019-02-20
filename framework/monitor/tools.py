# -*- coding: utf-8 -*-
from component.shortcuts import get_client_by_request
from common.log import logger
import base64
from account.models import *
from blueking.component.shortcuts import *
from gatherData.function import gather_data


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


def job_interface(res):
    try:
        params = res['params']  # ip
        gather_params = res['gather_params']
        bk_job_id = res['job_id'][0]['id']
        script_param = base64.b64encode (gather_params)
        user_account = BkUser.objects.filter(id=1).get()
        # 根据id为1的用户获取客户端操作快速执行脚本
        client = get_client_by_user(user_account)
        client.set_bk_api_ver('v2')
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
        else:
            job_list = []
            logger.error (u"请求作业模板失败：%s" % job.get ('message'))
        res1 = success_result(job_list)
        data = res1['results']['message']

    except Exception as e:
        res1 = error_result(e)
        data = res1['message']
    info = {
        'id': res['id'],  # 关联id
        'message': "message",  # 状态
        'message_value': data,  # 状态值
        'gather_params': 'space_interface'  # 类型
    }
    gather_data (info)
    return res1
