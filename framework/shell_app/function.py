# -*- coding: utf-8 -*-
from blueking.component.shortcuts import get_client_by_request
from common.mymako import render_json
from common.log import logger
from shell_app.models import UserCarouselBaseSetting
import uuid


def show_host(request):
    """
    取出所有主机信息
    :param request:
    :return:
    """
    clickPage_unicode = request.GET.get("clickPage")                # 获取页面页码数
    limit = 7                                                       # 定义页面长度
    if clickPage_unicode is None or clickPage_unicode == "":        # 页码数是否为空，空时赋值为第一页
        clickPage = 1
    else:
        clickPage = int(clickPage_unicode.encode("utf-8"))          # 对页码进行转码
    startPage = (clickPage - 1) * limit                             # 接口参数:数据起始页码
    try:
        client = get_client_by_request(request)                     # 获取code、secret参数
        bk_token = request.COOKIES.get("bk_token")                  # 获取token参数
        client.set_bk_api_ver('v2')                                 # 以v2版本调用接口
        display_list = []                                           # 定义一个空列表
        param = {                                                   # 以下定义search_host--查询主机接口参数
            "bk_app_code": client.app_code,
            "bk_app_secret": client.app_secret,
            "bk_token": bk_token,
            "ip": {
                "data": [],
                "exact": 1,
                "flag": "bk_host_innerip|bk_host_outerip"
            },
            "condition": [
                {
                    "bk_obj_id": "host",
                    "fields": [],
                    "condition": []
                },
                {
                    "bk_obj_id": "biz",
                    "fields": [],
                    "condition": [
                        {
                            "field": "bk_biz_id",
                            "operator": "$eq",
                            "value" : 2
                        }
                    ]
                },
            ],
            "page": {
                "start": 0,
                "limit": 20,
                "sort": "bk_host_id"
            },
            "pattern": ""
        }
        param2 = {                                                  # 定义get_agent_status--agent状态接口参数
            "bk_app_code": client.app_code,
            "bk_app_secret": client.app_secret,
            "bk_token": bk_token,
            "bk_supplier_id": 0,
            "hosts": [
                {
                    "ip": 0,
                    "bk_cloud_id": "0"
                }
            ]
        }
        res = client.cc.search_host(param)                          # 调用search_host接口
        if res.get('result', False):                                # 判断调用search_host接口是否成功，成功则取数据，失败则返回错误信息
            bk_host_list = res.get('data').get('info')
        else:
            bk_host_list = []
            logger.error(u"请求主机列表失败：%s" % res.get('message'))
        for i in bk_host_list:                                      # 循环遍历接口返回的参数，取出数据保存
            dic = {}
            dic['bk_os_name'] = i['host']['bk_os_name']
            dic['bk_host_name'] = i['host']['bk_host_name']
            dic['bk_host_innerip'] = i['host']['bk_host_innerip']
            dic['bk_inst_name'] = i['host']['bk_cloud_id'][0]['bk_inst_name']
            param2['hosts'][0]['ip'] = dic['bk_host_innerip']
            res2 = client.gse.get_agent_status(param2)              # 调用get_agent_status接口
            bk_agent_info = res2['data']
            if bk_agent_info['0:'+dic['bk_host_innerip']]['bk_agent_alive'] == 1:
                dic['bk_agent_alive'] = u"Agent已安装"
            else:
                dic['bk_agent_alive'] = u"Agent未安装"
            display_list.append(dic)                                # 把取出来的数据保存到display_list里面
        return_dic = {
            "result": True,
            "message": u"成功",
            "code": 0,
            "results": display_list,
        }
        return return_dic                                        # 返回json数据
    except Exception as e:
        return_dic = {
            "result": False,
            "message": u"失败",
            "code": 0,
            "results": 0
        }
        return return_dic


def model_tree_host(request):
    """
    树状主机信息显示
    :param request:
    :return:
    """
    try:
        client = get_client_by_request(request)  # 获取code、secret参数
        bk_token = request.COOKIES.get("bk_token")  # 获取token参数
        # bk_inst_name = request.get('bk_inst_name')
        client.set_bk_api_ver('v2')  # 以v2版本调用接口
        param = {
            "bk_app_code": client.app_code,
            "bk_app_secret": client.app_secret,
            "bk_token": bk_token,
            "bk_biz_id": 2
            }
        res = client.cc.search_biz_inst_topo(param)
        if res.get('result', False):
            # 判断调用search_biz_inst_topo接口是否成功，成功则取数据，失败则返回错误信息
            bk_tree_list = res.get('data')
        else:
            bk_tree_list = []
            logger.error(u"请求主机拓扑列表失败：%s" % res.get('message'))
        test_list = bk_tree_list[0]['child'] # 取出集群数据
        dispaly_list = []
        for i in test_list:  # 循环遍历取出集群名称
            dic = {}
            child_list = []
            dic['bk_inst_name'] = i['bk_inst_name']
            dic['bk_inst_id'] = i['bk_inst_id']
            for child in i['child']:
                dic1 = {}
                dic1['child_bk_inst_name'] = child['bk_inst_name']
                dic1['child_bk_inst_id'] = child['bk_inst_id']
                child_list.append(dic1)
            dic['child'] = child_list
            dispaly_list.append(dic)
        return_dic = {
            "result": True,
            "message": u"成功",
            "code": 0,
            "results": dispaly_list
        }
        return return_dic

    except Exception as e:
        return_dic = {
            "result": False,
            "message": u"失败",
            "code": 0,
            "results": 0
        }
        return return_dic


def select_module_host(request):
    """
    此函数类似于show_host函数
    :param request:
    :return:
    """
    try:
        client = get_client_by_request(request)
        bk_token = request.COOKIES.get('bk_token')
        client.set_bk_api_ver('v2')
        param = {
            "bk_app_code": client.app_code,
            "bk_app_secret": client.app_secret,
            "bk_token": bk_token,
            "ip": {
                "data": [],
                "exact": 1,
                "flag": "bk_host_innerip|bk_host_outerip"
            },
            "condition": [
                {
                    "bk_obj_id": "host",
                    "fields": [
                    ],
                    "condition": []
                },
                {
                    "bk_obj_id": "biz",
                    "fields": [],
                    "condition": [
                        {
                            "field": "bk_biz_id",
                            "operator": "$eq",
                            "value": 2
                        }
                    ]
                },
                {
                    "bk_obj_id": "set",
                    "fields": [],
                    "condition": [
                        {
                            "field": "bk_set_id",
                            "operator": "$eq",
                            "value": 7
                        }
                    ]
                },
                {
                    "bk_obj_id": "module",
                    "fields": [],
                    "condition": [
                        {
                            "field": "bk_module_id",
                            "operator": "$eq",
                            "value": 34
                        }
                    ]
                },

            ],
            "page": {
                "sort": "bk_host_id"
            },
            "pattern": ""
        }
        param2 = {  # 定义get_agent_status--agent状态接口参数
            "bk_app_code": client.app_code,
            "bk_app_secret": client.app_secret,
            "bk_token": bk_token,
            "bk_supplier_id": 0,
            "hosts": [
                {
                    "ip": 0,
                    "bk_cloud_id": "0"
                }
            ]
        }
        res = client.cc.search_host(param)
        if res.get('result',False):
            module_list = res.get('data')
        else:
            module_list = []
            logger.error(u"请求module信息失败：%s" % res.get ('message'))
        display_list = []
        for_list = module_list['info']
        x=0
        for i in for_list:
            dic = {}
            dic['bk_host_name'] = i['host']['bk_host_name']
            dic['bk_host_innerip'] = i['host']['bk_host_innerip']
            param2['hosts'][0]['ip'] = dic['bk_host_innerip']
            res2 = client.gse.get_agent_status(param2)                     # 调用get_agent_status接口
            bk_agent_info = res2['data']
            if bk_agent_info['0:' + dic['bk_host_innerip']]['bk_agent_alive'] == 1:
                dic['bk_agent_alive'] = u"Agent已安装"
            else:
                dic['bk_agent_alive'] = u"Agent未安装"
            display_list.append(dic)
        count = module_list['count']
        print(count)
        return_dic= {
            'results': display_list,
            'count': count
            }
        return return_dic

    except Exception as e:
        return render_json(
            {
                'results':'失败'
            }
        )


def get_user(request):
    """
    获取当前用户
    :param request:
    :return:
    """
    try:
        client = get_client_by_request(request)  # 获取code、secret参数
        bk_token = request.COOKIES.get("bk_token")  # 获取token参数
        client.set_bk_api_ver('v2')  # 以v2版本调用接口
        param = {
            "bk_app_code": client.app_code,
            "bk_app_secret": client.app_secret,
            "bk_token": bk_token,
        }
        result = client.bk_login.get_user(param)  # 获取当前用户信息
    except Exception, e:
        result = {
            "result": False,
            "message": u"失败 %s" % e,
            "code": 0,
            "results": 0
        }
    return result


def error_result(e):
    """
    失败统一JSON
    :param e:
    :return:
    """
    result = {
        "result": False,
        "message": u"失败 %s" % e,
        "code": 0,
        "results": 0
    }
    return result


def user_carousel(request):
    """
    用户修改Carousel设置
    :param request:
    :return:
    """
    carousel_time = request.GET.get("carousel_time")                            # 轮播时间
    carousel_number = request.GET.get("carousel_number")                        # 轮播数量
    carousel_id = uuid.uuid1()                                                  # 轮播ID
    try:
        user_info = get_user(request)
        bk_username = user_info.get('data').get('bk_username')                  # 当前用户用户名
        temp_result = UserCarouselBaseSetting.objects.get_carousel(bk_username)
        if temp_result.get('code') is True:                                     # 判断是否存在当前用户
            if carousel_time is None:
                carousel_time = '4000'
            if carousel_number is None:
                carousel_number = '5'
            data = {
                'bk_username': bk_username,
                'carousel_time': carousel_time,
                'carousel_number': carousel_number,
                'carousel_id': carousel_id,
            }
            result = UserCarouselBaseSetting.objects.update_carousel(bk_username, data)
        else:                                                                   # 新增用户Carousel设置
            if carousel_time is None:
                carousel_time = '3000'
            if carousel_number is None:
                carousel_number = '3'
            data = {
                'bk_username': bk_username,
                'carousel_time': carousel_time,
                'carousel_number': carousel_number,
                'carousel_id': carousel_id,
            }
            result = UserCarouselBaseSetting.objects.save_carousel(data)
    except Exception, e:
        result = error_result(e)
    return result


def get_user_carousel_time(request):
    """
    获取Carousel设置的时间与轮播数量
    :param request:
    :return:
    """
    try:
        user_info = get_user(request)
        bk_username = user_info.get('data').get('bk_username')              # 当前用户用户名
        result = UserCarouselBaseSetting.objects.get_carousel(bk_username)
    except Exception, e:
        result = error_result(e)
    return result
