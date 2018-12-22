# -*- coding: utf-8 -*-
from blueking.component.shortcuts import get_client_by_request
from common.mymako import render_json
from common.log import logger
from shell_app.models import UserCarouselBaseSetting
from shell_app.models import StaffInfo
from shell_app.models import StaffPosition
from shell_app.models import Scene
from shell_app.models import StaffScene
from shell_app.models import PositionScene
import uuid
import json
import time
import datetime
from django.db import connection


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
        "code": 1,
        "results": 0
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


def get_staff_info(request):
    """
    通过用户名获取职员信息-完成
    :param request:
    :return:
    """
    try:
        user_info = get_user(request)
        bk_username = user_info.get('data').get('bk_username')              # 当前用户用户名
        result = StaffInfo.objects.get_staff_info(bk_username)
    except Exception, e:
        result = error_result(e)
    return result


def save_staff_info(request):
    """
    保存员工信息--待完善
    :param request:
    :return:
    """
    try:
        user_info = get_user(request)
        bk_username = user_info.get('data').get('bk_username')  # 当前用户用户名
        staff_position_id = 1                                   # 假定岗位ID为1,待完善
        temp_result = StaffInfo.objects.get_staff_info(bk_username)
        temp_code = temp_result.get("code")
        if temp_code is True:                                   # 判断是否存在该员工信息表
            result = temp_result
        else:
            data = {
                "bk_username": bk_username,
                "staff_position_id": staff_position_id,
            }
            result = StaffInfo.objects.save_staff_info(data)
    except Exception, e:
        result = error_result(e)
    return result


def get_staff_position_by_username(request):
    """
    获取岗位信息--完成
    :param request:
    :return:
    """
    try:
        user_info = get_staff_info(request)
        staff_position_id = user_info.get("result").get("staff_position_id")
        temp_result = StaffPosition.objects.get_staff_position_by_username(staff_position_id)
        result = temp_result
    except Exception, e:
        result = error_result(e)
    return result


def get_scene_by_staff_position_id(request):
    """
    根据用户ID获取场景信息----未添加时间
    :param request:
    :return:
    """
    try:
        staff_position = get_staff_position_by_username(request)                                      # 获取场景信息
        staff_position_id = staff_position.get("result").get("staff_position_id")                     # 场景ID
        str_now_time = time.strftime("%H:%M:%S", time.localtime(time.time()))
        now_time = time.localtime(time.time())
        # print now_time
        # print type(now_time)
        # print str_now_time
        # print type(str_now_time)
        temp_result = Scene.objects.get_scene_by_staff_position_id(staff_position_id).get("result")  # 场景信息结果
        result = success_result(temp_result)
        return result
    except Exception, e:
        result = error_result(e)
        return result


def get_scene_by_staff_position_id_time_order_by_scene_order_id(request):
    """
    根据用户ID和当前时间获取场景信息
    :param request:json
    :return:
    """
    try:
        staff_position = get_staff_position_by_username(request)                                # 获取场景信息
        staff_position_id = staff_position.get("result").get("staff_position_id")               # 场景ID
        now_time = datetime.datetime.now().strftime("%H:%M:%S")                                 # 当前时间
        temp_result = Scene.objects.get_scene_by_staff_position_id_time_order_by_scene_order_id(staff_position_id,
                                                                                                now_time).get("result")
        result = success_result(temp_result)
    except Exception, e:
        result = error_result(e)
    return result


def save_staff_scene(request):
    """
    保存用户自定义设置
    :param request:
    :return:
    """
    scene_res = get_scene_by_staff_position_id(request)
    user_info = get_user(request)
    bk_username = user_info.get('data').get('bk_username')                                      # 当前用户用户名
    staff_scene_default_time = 6000                                                             # 用户自定义设置默认事件
    list = []
    for i in scene_res.get("results"):
        print i['scene_id']
        print bk_username
        data = {
            "staff_scene_id": i['scene_id'],
            "staff_scene_order_id": i['scene_order_id'],
            "bk_username": bk_username,
            "staff_scene_default_time": "staff_scene_default_time",
        }
        res = StaffScene.objects.save_staff_scene(data)
        list.append(res)
    result = success_result(list)
    return result


def get_staff_scene_test(request):
    """
    获取场景 ---- 完成-----一个岗位对应多个场景
    :param request:
    :return:
    """
    user_info = get_user(request)                                                   # 获取当前用户信息
    bk_username = user_info.get('data').get('bk_username')                          # 当前用户用户名
    staff_position = get_staff_position_by_username(request)                        # 获取场景信息
    staff_position_id = staff_position.get("result").get("staff_position_id")       # 获取职位ID
    now_time = datetime.datetime.now().strftime("%H:%M:%S")                         # 当前时间字符串型
    # 根据岗位获取对应场景信息
    scene_res = Scene.objects.filter(staff_position_id=staff_position_id, scene_start_time__lt=now_time,
                                     scene_stop_time__gt=now_time).order_by('scene_order_id').values()
    scene_list = []                                                                 # 所有符合要求的场景id
    for i in scene_res:                                                             # 遍历结果集
        scene_id = i['scene_id']
        scene_list.append(scene_id)
    print scene_list
    # 根据用户和场景ID遍历个人设置场景信息(根据用户设置排序)
    staff_scene_res = StaffScene.objects.filter(bk_username=bk_username,
                                                staff_scene_id__in=scene_list).order_by('staff_scene_order_id').values()
    staff_scene_list = []                                                           # 用户设置了的并符合要求的场景ID
    staff_scene_default_time_list = []
    for i in staff_scene_res:
        staff_scene_id = i['staff_scene_id']
        staff_scene_list.append(staff_scene_id)
        staff_scene_default_time = i['staff_scene_default_time']
        staff_scene_default_time_list.append(staff_scene_default_time)
    print staff_scene_list
    print staff_scene_default_time_list
    difference_list = list(set(scene_list).difference(set(staff_scene_list)))       # 用户没有设置的场景ID,将默认排在最后
    print difference_list
    temp = StaffScene.objects.filter(bk_username=bk_username, staff_scene_id__in=scene_list).values()
    temp_list = []
    for i in temp:
        temp_list.append(i)
    print temp_list.__len__()
    result_list = []                                                                # 存储最后结果集

    staff_scene_default_time_list_length = 0
    for j in staff_scene_list:
        # 将符合要求的并且用户设置了顺序的依次添加搞结果集
        result = Scene.objects.filter(scene_id=j, scene_start_time__lt=now_time,
                                      scene_stop_time__gt=now_time).values()
        for i in result:
            i['scene_start_time'] = i['scene_start_time'].strftime("%H:%M:%S")
            i['scene_stop_time'] = i['scene_stop_time'].strftime("%H:%M:%S")
            i['scene_default_time'] = staff_scene_default_time_list[staff_scene_default_time_list_length]
            staff_scene_default_time_list_length = staff_scene_default_time_list_length + 1
            result_list.append(i)

    # 取出符合要求的并且用户没有自主设置的场景添
    temp_staff_scene = Scene.objects.filter(staff_position_id=staff_position_id, scene_start_time__lt=now_time,
                                            scene_stop_time__gt=now_time,
                                            scene_id__in=difference_list).order_by('scene_order_id').values()
    # 将符合要求的并且用户没有自主设置的场景添加到结果集
    for i in temp_staff_scene:
        i['scene_start_time'] = i['scene_start_time'].strftime("%H:%M:%S")
        i['scene_stop_time'] = i['scene_stop_time'].strftime("%H:%M:%S")
        result_list.append(i)
    result = success_result(result_list)
    return result


def get_staff_scene(request):
    """
    获取场景 ---- 完成-----多个岗位对应多个场景
    :param request:
    :return:
    """
    try:
        staff_info = get_staff_info(request)
        now_time = datetime.datetime.now().strftime("%H:%M:%S")                 # 当前时间字符串型
        bk_username = staff_info.get('result').get('bk_username')               # 当前用户用户名
        # res = PositionScene.objects.get_position_scene(staff_info.get("result").get("staff_position_id"))
        res = PositionScene.objects.get_position_scene(2)
        temp_list = []                                                          # 存储scene_id
        for i in res.get("result"):
            temp_list.append(i['scene_id'])
        pass
        print (u'通过岗位获取的所有岗位有的场景ID')
        print temp_list
        # 根据岗位获取对应场景信息
        scene_res = Scene.objects.filter(scene_id__in=temp_list, scene_start_time__lt=now_time,
                                         scene_stop_time__gt=now_time).order_by('scene_order_id').values()
        scene_list = []                                                         # 所有符合要求的场景id
        for i in scene_res:                                                     # 遍历结果集
            scene_id = i['scene_id']
            scene_list.append(scene_id)
        print (u"符合要求的场景ID")
        print scene_list
        # 根据用户和场景ID遍历个人设置场景信息(根据用户设置排序)
        staff_scene_res = StaffScene.objects.filter(bk_username=bk_username,
                                                    staff_scene_id__in=scene_list).order_by(
                                                    'staff_scene_order_id').values()
        staff_scene_list = []                                                   # 用户设置了的并符合要求的场景ID
        staff_scene_default_time_list = []
        for i in staff_scene_res:
            staff_scene_id = i['staff_scene_id']
            staff_scene_list.append(staff_scene_id)
            staff_scene_default_time = i['staff_scene_default_time']
            staff_scene_default_time_list.append(staff_scene_default_time)
        print (u'用户设置了的场景ID')
        print staff_scene_list
        print (u'用户自定义设置的时间')
        print staff_scene_default_time_list
        difference_list = list(set(scene_list).difference(set(staff_scene_list)))  # 用户没有设置的场景ID,将默认排在最后
        print (u'用户没有设置的场景ID')
        print difference_list
        temp = StaffScene.objects.filter(bk_username=bk_username, staff_scene_id__in=scene_list).values()
        temp_list = []
        for i in temp:
            temp_list.append(i)
        result_list = []  # 存储最后结果集
        staff_scene_default_time_list_length = 0
        for j in staff_scene_list:
            # 将符合要求的并且用户设置了顺序的依次添加搞结果集
            result = Scene.objects.filter(scene_id=j, scene_start_time__lt=now_time,
                                          scene_stop_time__gt=now_time).values()
            for i in result:
                i['scene_start_time'] = i['scene_start_time'].strftime("%H:%M:%S")
                i['scene_stop_time'] = i['scene_stop_time'].strftime("%H:%M:%S")
                i['scene_default_time'] = staff_scene_default_time_list[staff_scene_default_time_list_length]
                staff_scene_default_time_list_length = staff_scene_default_time_list_length + 1
                result_list.append(i)

        # 取出符合要求的并且用户没有自主设置的场景添
        temp_staff_scene = Scene.objects.filter(scene_start_time__lt=now_time,
                                                scene_stop_time__gt=now_time,
                                                scene_id__in=difference_list).order_by('scene_order_id').values()
        # 将符合要求的并且用户没有自主设置的场景添加到结果集
        for i in temp_staff_scene:
            i['scene_start_time'] = i['scene_start_time'].strftime("%H:%M:%S")
            i['scene_stop_time'] = i['scene_stop_time'].strftime("%H:%M:%S")
            result_list.append(i)
        result = success_result(result_list)
    except Exception, e:
        result = error_result(e)
    return result


def get_test_json(request):
    """
    function函数专用测试json数据
    :param request:
    :return: json
    """
    try:
        staff_info = get_staff_info(request)
        now_time = datetime.datetime.now().strftime("%H:%M:%S")                 # 当前时间字符串型
        bk_username = staff_info.get('result').get('bk_username')               # 当前用户用户名
        # res = PositionScene.objects.get_position_scene(staff_info.get("result").get("staff_position_id"))
        res = PositionScene.objects.get_position_scene(2)
        temp_list = []                                                          # 存储scene_id
        for i in res.get("result"):
            temp_list.append(i['scene_id'])
        pass
        print (u'通过岗位获取的所有岗位有的场景ID')
        print temp_list
        # 根据岗位获取对应场景信息
        scene_res = Scene.objects.filter(scene_id__in=temp_list, scene_start_time__lt=now_time,
                                         scene_stop_time__gt=now_time).order_by('scene_order_id').values()
        scene_list = []                                                         # 所有符合要求的场景id
        for i in scene_res:                                                     # 遍历结果集
            scene_id = i['scene_id']
            scene_list.append(scene_id)
        print (u"符合要求的场景ID")
        print scene_list
        # 根据用户和场景ID遍历个人设置场景信息(根据用户设置排序)
        staff_scene_res = StaffScene.objects.filter(bk_username=bk_username,
                                                    staff_scene_id__in=scene_list).order_by(
                                                    'staff_scene_order_id').values()
        staff_scene_list = []                                                   # 用户设置了的并符合要求的场景ID
        staff_scene_default_time_list = []
        for i in staff_scene_res:
            staff_scene_id = i['staff_scene_id']
            staff_scene_list.append(staff_scene_id)
            staff_scene_default_time = i['staff_scene_default_time']
            staff_scene_default_time_list.append(staff_scene_default_time)
        print (u'用户设置了的场景ID')
        print staff_scene_list
        print (u'用户自定义设置的时间')
        print staff_scene_default_time_list
        difference_list = list(set(scene_list).difference(set(staff_scene_list)))  # 用户没有设置的场景ID,将默认排在最后
        print (u'用户没有设置的场景ID')
        print difference_list
        temp = StaffScene.objects.filter(bk_username=bk_username, staff_scene_id__in=scene_list).values()
        temp_list = []
        for i in temp:
            temp_list.append(i)
        result_list = []  # 存储最后结果集
        staff_scene_default_time_list_length = 0
        for j in staff_scene_list:
            # 将符合要求的并且用户设置了顺序的依次添加搞结果集
            result = Scene.objects.filter(scene_id=j, scene_start_time__lt=now_time,
                                          scene_stop_time__gt=now_time).values()
            for i in result:
                i['scene_start_time'] = i['scene_start_time'].strftime("%H:%M:%S")
                i['scene_stop_time'] = i['scene_stop_time'].strftime("%H:%M:%S")
                i['scene_default_time'] = staff_scene_default_time_list[staff_scene_default_time_list_length]
                staff_scene_default_time_list_length = staff_scene_default_time_list_length + 1
                result_list.append(i)

        # 取出符合要求的并且用户没有自主设置的场景添
        temp_staff_scene = Scene.objects.filter(scene_start_time__lt=now_time,
                                                scene_stop_time__gt=now_time,
                                                scene_id__in=difference_list).order_by('scene_order_id').values()
        # 将符合要求的并且用户没有自主设置的场景添加到结果集
        for i in temp_staff_scene:
            i['scene_start_time'] = i['scene_start_time'].strftime("%H:%M:%S")
            i['scene_stop_time'] = i['scene_stop_time'].strftime("%H:%M:%S")
            result_list.append(i)
        result = success_result(result_list)
    except Exception, e:
        result = error_result(e)
    return result

def show_host1(request):
    try:

        bk_biz_id = request.GET.get('data')
        x = "{}".format(bk_biz_id)
        p = int(x)
        print(type(p))
        print(p)
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
                            "value" : p
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

def test(request):
    result = show_host1(request)
    res = result['results']

    x = 1
    display_list = []
    data = {}
    for i in res:
        dic = {}
        dic['index'] = x
        x += 1
        dic['bk_host_innerip'] = i['bk_host_innerip']
        dic['bk_os_name'] = i['bk_os_name']
        display_list.append(dic)
        if x == 5:
            break
    data['items'] = display_list

    return data

def create_task(request):
    """
    创建任务
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
            "name": "tasktest",
            "flow_type": "common",
            "bk_biz_id": "2",
            "template_id": "34",
            "constants": {
                "${content}": "echo 1",
                "${params}": "",
                "${script_timeout}": 20,
                },
            }
        res = client.sops.create_task(param)
        return res
    except Exception as e:
        dic = {'results': 0}
        return dic

def start_task(request):
    """
    开始任务
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
            "bk_biz_id": "2",
            "task_id": "590",
        }
        res = client.sops.start_task(param)

        return res
    except Exception as e:
        dic = {'results': 0}
        return dic


