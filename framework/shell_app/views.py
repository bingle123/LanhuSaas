# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from blueking.component.shortcuts import get_client_by_request
from common.mymako import render_json
from common.log import logger
def show_Host(request):
    """根据一个或者多个业务查询主机列表"""
    try:
        client = get_client_by_request (request)
        bk_token = request.COOKIES.get ("bk_token")
        #req = json.loads (request.body)
        #bk_biz_list = req.get("bk_biz_list")
        client.set_bk_api_ver ('v2')
        display_list = []
        #if bk_biz_list:
            #for i in bk_biz_list:
        param={
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
                "start": 0,
                "limit": 10,
                "sort": "bk_host_id"
            },
            "pattern": ""
        }
        param1 = {
            "bk_token": bk_token,
            "fields": [
                "bk_biz_id",
                "bk_biz_name"
            ],
        }
        res = client.cc.search_host(param)
        res1 = client.cc.search_business(param1)
        if res1.get('result', False):
            bk_biz_info = res1.get('data').get('info')
        else:
            bk_biz_info = {}
            logger.error(u"获取业务详情失败：%s" % res.get('message'))
        if res.get('result', False):
            bk_host_list = res.get('data').get('info')
        else:
            bk_host_list = []
            logger.error(u"请求主机列表失败：%s" % res.get('message'))
        dic = {

        }
        print(bk_biz_info)



        print(bk_host_list)
        return render_json(
            {
                "result": True,
                "message": u"查询执行历史数据成功",
                "code": 0,
                "results": bk_host_list
            }
        )




    except Exception as e:
        return render_json (
            {
                "result": True,
                "message": u"查询执行历史数据成功",
                "code": 0,
                "results": 1
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
