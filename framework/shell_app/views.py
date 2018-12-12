# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from blueking.component.shortcuts import get_client_by_request
from common.mymako import render_json
from common.mymako import render_mako_context
from common.log import logger

def showselect(request):
    """
    选择服务器页面
    :param request:
    :return: 选择服务器页面
    """
    return render_mako_context(request, './common/select.html')


def show_Host(request):
    """
    主机页面展示，包含分页功能
    :param request: clickPage:页码数
    :return:        json
    """
    clickPage_unicode = request.GET.get("clickPage")                # 获取页面页码数
    limit = 7                                                       # 定义页面长度
    if clickPage_unicode is None or clickPage_unicode == "":        # 页码数是否为空，空时赋值为第一页
        clickPage = 1
    else:
        clickPage = int(clickPage_unicode.encode("utf-8"))          # 对页码进行转码
    startPage = (clickPage - 1) * limit                             # 接口参数:数据起始页码
    print (11)
    print("liaomingtao")
    print (22)
    print ("chenyi")
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
                    "bk_obj_id": "object",
                    "fields": [],
                    "condition": [
                        {
                            "field": "bk_biz_id",
                            "operator": "$eq",

                        }
                    ]
                }
            ],
            "page": {
                "start": startPage,
                "limit": limit,
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
        return render_json({                                        # 返回json数据给前台
            "result": True,
            "message": u"成功",
            "code": 0,
            "results": display_list,
        })
    except Exception as e:
        return render_json({
                "result": False,
                "message": u"失败",
                "code": 0,
                "results": 0
            })


def modle_Tree_Host(request):
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
        # param1 = {
        #     "bk_app_code": client.app_code,
        #     "bk_app_secret": client.app_secret,
        #     "bk_token": bk_token,
        #     "fields": [
        #         "bk_module_name"
        #     ],
        #     # "condition": {
        #     #     "bk_module_name": "test"
        #     # },
        #     "page": {
        #         "start": 0,
        #         "limit": 100
        #     }
        # }
        res = client.cc.search_biz_inst_topo(param)
        # res1 = client.cc.search_module(param1)
        if res.get('result', False):
            #判断调用search_biz_inst_topo接口是否成功，成功则取数据，失败则返回错误信息
            bk_tree_list = res.get('data')
        else:
            bk_tree_list = []
            logger.error(u"请求主机拓扑列表失败：%s" % res.get('message'))
        # if res1.get('result', False):
        #     bk_module_list = res.get1('data')
        # else:
        #     bk_module_list = []
        #     logger.error(u"请求模块失败：%s" % res1.get('message'))
        print(bk_module_list)
        test_list = bk_tree_list[0]['child'] #取出集群数据
        dispaly_list = []
        for i in test_list:  #循环遍历取出集群名称
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
        return render_json(
            {
                "result": True,
                "message": u"成功",
                "code": 0,
                "results": dispaly_list
            }
        )

    except Exception as e:
        return render_json (
            {
                "result": False,
                "message": u"失败",
                "code": 0,
                "results": 0
            }
        )
def modle_Tree_Host1(request):
    try:
        client = get_client_by_request (request)  # 获取code、secret参数
        bk_token = request.COOKIES.get ("bk_token")  # 获取token参数
        bk_inst_id = 7
        client.set_bk_api_ver ('v2')  # 以v2版本调用接口
        param = {
            "bk_app_code": client.app_code,
            "bk_app_secret": client.app_secret,
            "bk_token": bk_token,
            "bk_biz_id": 2
        }
        res = client.cc.search_biz_inst_topo (param)
        if res.get ('result', False):
            # 判断调用search_biz_inst_topo接口是否成功，成功则取数据，失败则返回错误信息
            bk_tree_list = res.get ('data')
        else:
            bk_tree_list = []
            logger.error (u"请求主机拓扑列表失败：%s" % res.get ('message'))
        test_list = bk_tree_list[0]['child']  # 取出集群数据
        dispaly_list = []
        bk_inst_list = []
        for i in test_list:
            if i['bk_inst_id'] == bk_inst_id:
                bk_inst_list.append(i)
                break
        print(bk_inst_list)
        for i in bk_inst_list:  # 循环遍历取出集群名称
            dic = {}
            dic['bk_inst_name'] = i[0]['child'][0]['bk_inst_name']

            dispaly_list.append (dic)
        return render_json (
            {
                "result": True,
                "message": u"成功",
                "code": 0,
                "results": bk_inst_list
            }
        )

    except Exception as e:
        return render_json (
            {
                "result": False,
                "message": u"失败",
                "code": 0,
                "results": 0
            }
        )

# def run_shell_host(request):
#     client = get_client_by_request(request)
#
#     client.set_bk_api_ver('v2')
#     if request.method == 'GET':
#         return render(request, 'base.html')
#     else:
#         list = []
#         bk_token = request.COOKIES.get ("bk_token")
#         req = json.loads(request.body)
#         bk_app_code = client.app_code
#         bk_app_secret = client.app_secret
#         list = req.get("list") #接收前台传来数据
#         client.set_bk_api_ver ('v2')
#         if list:
#             for i in list:
#                 print list
#                 param = {
#                     "bk_app_code": bk_app_code,
#                     "bk_app_secret": bk_app_secret,
#                     "bk_token": bk_token,
#                     "bk_biz_id": list.bk_biz_id,
#                     "script_id": list.script_id,
#                     #"script_content": "ZWNobyAkMQ==",
#                     #"script_param": "aGVsbG8=",
#                     "script_timeout": 1000,
#                     "account": list.account,
#                     "is_param_sensitive": 0,
#                     "script_type": list.script_type,
#                     "ip_list": [
#                         {
#                             "bk_cloud_id": list.bk_cloud_id,
#                             "ip": list.ip
#                         },
#                         {
#                             "bk_cloud_id": list.bk_cloud_id,
#                             "ip": list.ip
#                         }
#                     ],
#                     "custom_query_id": [
#                         "3"
#                     ]
#                 }
#             res = client.job.fast_execute_script(param)
#             list1 = []
#             dic = {
#                 "bk_biz_name":"name",
#                 "script_name":"name",
#                 #.....
#                 #前台展示的各项数据
#             }
#             if res.get('result',False):
#                 message = res.get('message')
#                 dic['message'] = message
#                 list1.append(dic)
#             return render_json (
#                 {
#                     "result": True,
#                     "message": u"执行脚本成功",
#                     "code": 0,
#                     "results": list1
#                 }
#             )
