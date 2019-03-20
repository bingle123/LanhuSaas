# -*- coding: utf-8 -*-
from common.mymako import render_json
from common.log import logger
from shell_app.models import StaffInfo
from shell_app.models import StaffPosition
from shell_app.models import Scene
from shell_app.models import StaffScene
from shell_app.models import PositionScene
from shell_app import tools
import uuid
import time
import datetime
import json
import random


def show_host(request):
    """
    取出所有主机信息
    :param request:
    :return:
    """
    limit = 7                            # 暂时为7
    bk_biz_id = 2
    start_page = tools.page_paging(request, limit)                          # 起始页码
    try:
        display_list = []                                                   # 定义一个空列表
        param = {                                                   # 以下定义search_host--查询主机接口参数
            "ip": {
                "data": [],
                "exact": 1,
                "flag": "bk_host_innerip|bk_host_outerip"
            },
            "condition": [
                {
                    "bk_obj_id": "biz",
                    "fields": [],
                    "condition": [
                        {
                            "field": "bk_biz_id",
                            "operator": "$eq",
                            "value": bk_biz_id
                        }
                    ]
                },
            ],
            "page": {
                "start": start_page,
                "limit": limit,
                "sort": "bk_host_id"
            },
        }
        param2 = {                                                  # 定义get_agent_status--agent状态接口参数
            "bk_supplier_id": 0,
            "hosts": [
                {
                    "ip": 0,
                    "bk_cloud_id": "0"
                }
            ]
        }
        client = tools.interface_param(request)
        res = client.cc.search_host(param)                                  # 调用search_host接口
        # 判断调用search_host接口是否成功，成功则取数据，失败则返回错误信息
        if res.get('result'):
            bk_host_list = res.get('data').get('info')
        else:
            bk_host_list = []
            logger.error(u"请求主机列表失败：%s" % res.get('message'))
        for i in bk_host_list:                                              # 循环遍历接口返回的参数，取出数据保存
            dic = {
                'bk_os_name': i['host']['bk_os_name'],
                'bk_host_name': i['host']['bk_host_name'],
                'bk_host_innerip': i['host']['bk_host_innerip'],
                'bk_inst_name':i['host']['bk_cloud_id'][0]['bk_inst_name'],
            }
            param2['hosts'][0]['ip'] = dic['bk_host_innerip']
            res2 = client.gse.get_agent_status(param2)                      # 调用get_agent_status接口
            bk_agent_info = res2['data']
            if bk_agent_info['0:'+dic['bk_host_innerip']]['bk_agent_alive'] == 1:
                dic['bk_agent_alive'] = u"Agent已安装"
            else:
                dic['bk_agent_alive'] = u"Agent未安装"
            display_list.append(dic)                                        # 把取出来的数据保存到display_list里面
        print display_list
        result = tools.success_result(display_list)
    except Exception, e:
        result = tools.error_result(e)
    return result


def model_tree_host(request):
    """
    树状主机信息显示
    :param request:
    :return:
    """
    try:
        param = {"bk_biz_id": 2}
        client = tools.interface_param(request)
        res = client.cc.search_biz_inst_topo(param)
        if res.get('result'):
            # 判断调用search_biz_inst_topo接口是否成功，成功则取数据，失败则返回错误信息
            bk_tree_list = res.get('data')
        else:
            bk_tree_list = []
            logger.error(u"请求主机拓扑列表失败：%s" % res.get('message'))
        test_list = bk_tree_list[0]['child'] # 取出集群数据
        display_list = []
        for i in test_list:  # 循环遍历取出集群名称
            dic = {
                'bk_inst_name': i['bk_inst_name'],
                'bk_inst_id': i['bk_inst_id'],
            }
            child_list = []
            for child in i['child']:
                dic1 = {
                    'child_bk_inst_name': child['bk_inst_name'],
                    'child_bk_inst_id': child['bk_inst_id'],
                }
                child_list.append(dic1)
            dic['child'] = child_list
            display_list.append(dic)
        result = tools.success_result(display_list)
    except Exception, e:
        result = tools.error_result(e)
    return result


def select_module_host(request):
    """
    此函数类似于show_host函数
    :param request:
    :return:
    """
    try:
        param = {
            "ip": {
                "data": [],
                "exact": 1,
                "flag": "bk_host_innerip|bk_host_outerip"
            },
            "condition": [

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
        }
        param1 = {  # 定义get_agent_status--agent状态接口参数
            "bk_supplier_id": 0,
            "hosts": [
                {
                    "ip": 0,
                    "bk_cloud_id": "0"
                }
            ]
        }
        client = tools.interface_param(request)
        res = client.cc.search_host(param)
        if res.get('result',False):
            module_list = res.get('data')
        else:
            module_list = []
            logger.error(u"请求module信息失败：%s" % res.get ('message'))
        display_list = []
        for_list = module_list['info']
        for i in for_list:
            dic = {
                'bk_host_name': i['host']['bk_host_name'],
                'bk_host_innerip': i['host']['bk_host_innerip'],
            }

            param1['hosts'][0]['ip'] = dic['bk_host_innerip']
            res2 = client.gse.get_agent_status(param1)                     # 调用get_agent_status接口
            bk_agent_info = res2['data']
            if bk_agent_info['0:' + dic['bk_host_innerip']]['bk_agent_alive'] == 1:
                dic['bk_agent_alive'] = u"Agent已安装"
            else:
                dic['bk_agent_alive'] = u"Agent未安装"
            display_list.append(dic)
        count = module_list['count']
        return_dic = {
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
        client = tools.interface_param(request)
        result = client.bk_login.get_user({})  # 获取当前用户信息
    except Exception, e:
        result = tools.error_result(e)
    return result


def get_staff_info(request):
    """
    获取职员信息-完成
    :param request:
    :return:
    """
    try:
        user_info = get_user(request)
        bk_username = user_info.get('data').get('bk_username')              # 当前用户用户名
        result = StaffInfo.objects.get_staff_info(bk_username)
    except Exception, e:
        result = tools.error_result(e)
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
        result = tools.error_result(e)
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
        result = tools.error_result(e)
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
        temp_result = Scene.objects.get_scene_by_staff_position_id(staff_position_id).get("result")  # 场景信息结果
        result = tools.success_result(temp_result)
        return result
    except Exception, e:
        result = tools.error_result(e)
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
        res = PositionScene.objects.get_position_scene(staff_info.get("result").get("staff_position_id"))
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
        result = tools.success_result(result_list)
    except Exception, e:
        result = tools.error_result(e)
    return result


def get_positions_all():
    """
    获取所有岗位信息
    :return:  json--results--StaffPosition对象
    """
    try:
        res = StaffPosition.objects.get_positions_all().get("result")
        result = tools.success_result(res)
    except Exception, e:
        result = tools.error_result(e)
    return result


def get_scenes_all():
    """
    获取所有场景信息
    :return:
    """
    try:
        result = Scene.objects.get_scenes_all().get("result")
    except Exception, e:
        result = tools.error_result(e)
    return result


def get_scene_by_id(id):
    """
    根据场景ID获取场景对象
    :param id:
    :return:
    """
    res = Scene.objects.get_scenes_by_id(id)
    if res.get("code"):
        result_temp = res.get("result")
        result = tools.success_result(result_temp)
    else:
        result_temp = res.get("result")
        result = tools.error_result(result_temp)
    return result


def add_scene(scene):
    """
    增加场景信息
    :param scene:
    :return:
    """
    print scene
    temp_scene = {
        "scene_id": uuid.uuid1(),
        "scene_name": scene.get('name'),
        "scene_start_time": scene.get('start_time'),
        "scene_stop_time": scene.get('stop_time'),
        "scene_default_time": scene.get('default_time'),
        "scene_example": scene.get('example'),
        "scene_order_id": scene.get('order_id'),
        "scene_staff_position": scene.get('position'),
    }
    res = Scene.objects.add_scene(temp_scene)
    return res


def get_test_json(request):
    """
    function函数专用测试json数据
    :param request:
    :return: json
    """

    return None


def get_scene_by_staff_position_id_time_order_by_scene_order_id(request):
    """
    根据用户ID和当前时间获取场景信息----暂时保留---待废弃
    :param request:json
    :return:
    """
    try:
        staff_position = get_staff_position_by_username(request)                                # 获取场景信息
        staff_position_id = staff_position.get("result").get("staff_position_id")               # 场景ID
        now_time = datetime.datetime.now().strftime("%H:%M:%S")                                 # 当前时间
        temp_result = Scene.objects.get_scene_by_staff_position_id_time_order_by_scene_order_id(staff_position_id,
                                                                                                now_time).get("result")
        result = tools.success_result(temp_result)
    except Exception, e:
        result = tools.error_result(e)
    return result


def save_staff_scene(request):
    """
    保存用户自定义设置  ---- 需要更改
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
            "staff_scene_default_time": staff_scene_default_time,
        }
        res = StaffScene.objects.save_staff_scene(data)
        list.append(res)
    result = tools.success_result(list)
    return result


def get_guotai_system_info(request):
    """
    获取过国泰君安系统状态
    :param request:
    :return:
    """
    request_body = json.loads(request.body)
    type_id = request_body['type_id']
    if type_id == '1':
        # 总系统状态查询
        result_list = []
        res = {
            "status": int(random.uniform(0, 4)),
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        result_list.append(res)
    elif type_id == '2':
        # 报盘系统状态查询
        result_list = []
        res = {
            "status": int(random.uniform(0, 4)),
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        result_list.append(res)
    return tools.success_result(result_list)


