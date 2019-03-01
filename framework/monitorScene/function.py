# -*- coding: utf-8 -*-
from __future__ import division
import json
import math
from django.core.paginator import Paginator
from django.forms import model_to_dict
from models import Scene
from models import position_scene
from monitor_item.models import Scene_monitor, Monitor, Job,Scene_monitor
from monitor_item import tools
from position.models import JobInstance, Localuser
from gatherData.models import TDGatherData
import sys
from logmanagement.function import add_log, make_log_info, get_active_user
from db_connection.function import get_db
from gatherData.function import gather_data
import datetime

def monitor_show(request):
    monitor = Scene.objects.all()
    res_list = []
    for i in monitor:
        dic = {
            'id': i.id,
            'scene_name': i.scene_name,
            'scene_startTime': str (i.scene_startTime),
            'scene_endTime': str (i.scene_endTime),
            'scene_creator': i.scene_creator,
            'scene_creator_time': str (i.scene_creator_time),
            'scene_editor': i.scene_editor,
            'scene_editor_time': str (i.scene_editor_time),
            'pos_name': ''
        }
        position = position_scene.objects.filter (scene=i.id)
        for c in position:
            job = JobInstance.objects.filter (id=c.position_id)
            for j in job:
                jobs = {
                    "pos_name": j.pos_name
                }
                dic['pos_name'] = jobs["pos_name"]
        res_list.append (dic)
    return res_list


def addSence(request):
    try:
        res = request.body
        senceModel = json.loads (res)
        senceModel2 = {
            "scene_name": senceModel['data']['scene_name'],
            "scene_startTime": senceModel['data']["scene_startTime"],
            "scene_endTime": senceModel['data']["scene_endTime"],
            "scene_creator": "admin"
        }
        Scene.objects.create (**senceModel2)
        id = Scene.objects.last ()
        senceModel3 = {
            "scene": id,
            "position_id": senceModel['data']["pos_name"]
        }
        position_scene.objects.create (**senceModel3)
        for i in senceModel['monitor_data']:
            print(i)
            monitor_data = {
                'scene_id': id.id,
                'item_id': int(i['item_id']),
                'x': int(i['x']),
                'y': int(i['y']),
                'scale': i['scale'],
                'score': int(i['score']),
                'order': int(i['order'])
            }
            Scene_monitor.objects.create (**monitor_data)
        info = make_log_info(u'增加场景', u'业务日志', u'position_scene', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'增加场景', u'业务日志', u'position_scene', sys._getframe().f_code.co_name,
                              get_active_user(request)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return None


def select_table(request):
    res = request.body
    res_list = []
    monitor = Scene.objects.filter (scene_name__contains=res)
    for i in monitor:
        dic = {
            'id': i.id,
            'scene_name': i.scene_name,
            'scene_startTime': str (i.scene_startTime),
            'scene_endTime': str (i.scene_endTime),
            'scene_creator': i.scene_creator,
            'scene_creator_time': str (i.scene_creator_time),
            'scene_editor': i.scene_editor,
            'scene_editor_time': str (i.scene_editor_time),
        }
        position = position_scene.objects.filter (scene=i.id)
        for c in position:
            job = JobInstance.objects.filter (id=c.position_id)
            for j in job:
                jobs = {
                    "pos_name": j.pos_name
                }
                dic['pos_name'] = jobs["pos_name"]
        res_list.append (dic)
        print res_list
    return res_list


def delect(request):
    try:
        Scene.objects.filter (id=request.body).delete ()
        position_scene.objects.filter (scene=request.body).delete ()
        info = make_log_info (u'删除场景', u'业务日志', u'position_scene', sys._getframe ().f_code.co_name,
                              get_active_user (request)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info (u'删除场景', u'业务日志', u'position_scene', sys._getframe ().f_code.co_name,
                              get_active_user (request)['data']['bk_username'], '失败', repr (e))
    add_log (info)
    return ""


def editSence(request):
    try:
        model = json.loads (request.body)
        senceModel2 = {
            "scene_name": model['data']['scene_name'],
            "scene_startTime": model['data']["scene_startTime"],
            "scene_endTime": model['data']["scene_endTime"],
            "scene_editor": "admin"
        }
        Scene.objects.filter (id=model['data']['id']).update (**senceModel2)
        info = make_log_info (u'编辑场景', u'业务日志', u'Scene', sys._getframe ().f_code.co_name,
                              get_active_user (request)['data']['bk_username'], '成功', '无')
        add_log (info)
        scene = Scene.objects.get (id=model['data']['id'])
        scene.save ()
        job = JobInstance.objects.filter (pos_name=model['data']["pos_name"])
        for j in job:
            senceModel3 = {
                "scene_id": model['data']['id'],
                "position_id": j.id
            }
            print senceModel3
        position_scene.objects.filter (scene=senceModel3['scene_id']).update (**senceModel3)
        info2 = make_log_info (u'编辑场景', u'业务日志', u'position_scene', sys._getframe ().f_code.co_name,
                               get_active_user (request)['data']['bk_username'], '成功', '无')
        add_log (info2)
    except Exception as e:
        info = make_log_info (u'编辑场景', u'业务日志', u'Scene', sys._getframe ().f_code.co_name,
                              get_active_user (request)['data']['bk_username'], '失败', repr (e))
        add_log (info)
        info2 = make_log_info (u'编辑场景', u'业务日志', u'Monitor', sys._getframe ().f_code.co_name,
                               get_active_user (request)['data']['bk_username'], '失败', repr (e))
        add_log (info2)
    return None


def scene_data(id):
    try:
        obj = Scene_monitor.objects.filter(scene_id=id)
        data_list = []
        for i in obj:
            data_dic = model_to_dict(i)
            data_dic['scale'] = str(i.scale)
            monitor_data = Monitor.objects.filter(id=data_dic['item_id'])
            data_list.append(data_dic)
        res = tools.success_result(data_list)
    except Exception as e:
        res = tools.error_result(e)
    return res


def pos_name(request):
    job = JobInstance.objects.all()
    res_list = []
    for i in job:
        dic = {
            'id': i.id,
            'pos_name': i.pos_name
        }
        res_list.append (dic)
    return res_list


def paging(request):
    res = json.loads (request.body)
    page = res['page']
    limit = res['limit']
    start_page = limit * page - 9
    monitor = Scene.objects.all ()[start_page - 1:start_page + 9]
    monitor2 = Scene.objects.all ().values ('id')
    page_count = math.ceil (len (monitor2) / 10)
    res_list = []
    for i in monitor:
        dic = {
            'id': i.id,
            'scene_name': i.scene_name,
            'scene_startTime': str (i.scene_startTime),
            'scene_endTime': str (i.scene_endTime),
            'scene_creator': i.scene_creator,
            'scene_creator_time': str (i.scene_creator_time),
            'scene_editor': i.scene_editor,
            'scene_editor_time': str (i.scene_editor_time),
            'pos_name': '',
            'page_count': page_count,
        }
        position = position_scene.objects.filter (scene=i.id)
        for c in position:
            job = JobInstance.objects.filter (id=c.position_id)
            for j in job:
                jobs = {
                    "pos_name": j.pos_name
                }
                dic['pos_name'] = jobs["pos_name"]
        res_list.append (dic)
    return res_list

# 场景编排显示
def scene_show(res):
    try:
        type = res['type']
        limit = res['limit']
        page = res['page']
        if type == 0:
            base_unit = Monitor.objects.filter (monitor_type='基本单元类型')
            base_page_data, base_page_count = tools.page_paging (base_unit, limit, page)
            chart_unit = Monitor.objects.filter (monitor_type='图表单元类型')
            chart_page_data, chart_page_count = tools.page_paging (chart_unit, limit, page)
            job_unit = Monitor.objects.filter (monitor_type='作业单元类型')
            job_page_data, job_page_count = tools.page_paging (job_unit, limit, page)
            flow_unit = Monitor.objects.filter (monitor_type='流程单元类型')
            flow_page_data, flow_page_count = tools.page_paging (flow_unit, limit, page)
            base_list = tools.obt_dic (base_page_data, base_page_count)
            chart_list = tools.obt_dic (chart_page_data, chart_page_count)
            job_list = tools.obt_dic (job_page_data, job_page_count)
            flow_list = tools.obt_dic (flow_page_data, flow_page_count)
            res_dic = {
                'base_list': base_list,
                'chart_list': chart_list,
                'job_list': job_list,
                'flow_list': flow_list,
            }
        elif type == 1:
            base_unit = Monitor.objects.filter (monitor_type='基本单元类型')
            base_page_data, base_page_count = tools.page_paging (base_unit, limit, page)
            base_list = tools.obt_dic (base_page_data, base_page_count)
            res_dic = {
                'base_list': base_list,
            }
        elif type == 2:
            chart_unit = Monitor.objects.filter (monitor_type='图表单元类型')
            chart_page_data, chart_page_count = tools.page_paging (chart_unit, limit, page)
            chart_list = tools.obt_dic (chart_page_data, chart_page_count)
            res_dic = {
                'chart_list': chart_list,
            }
        elif type == 3:
            job_unit = Monitor.objects.filter (monitor_type='作业单元类型')
            job_page_data, job_page_count = tools.page_paging (job_unit, limit, page)
            job_list = tools.obt_dic (job_page_data, job_page_count)
            job_status_list = []
            for i in job_list:
                try:
                    job_status = Job.objects.filter (job_id=i['jion_id']).last ().status
                except Exception as e:
                    job_status = 0
                job_status_list.append (job_status)
            for i in range (0, len (job_status_list)):
                job_list[i]['job_status'] = job_status_list[i]
            res_dic = {
                'job_list': job_list,
            }
        elif type == 4:
            flow_unit = Monitor.objects.filter (monitor_type='流程单元类型')
            flow_page_data, flow_page_count = tools.page_paging (flow_unit, limit, page)
            flow_list = tools.obt_dic (flow_page_data, flow_page_count)
            res_dic = {
                'flow_list': flow_list,
            }
        result = tools.success_result (res_dic)
    except Exception as e:
        result = tools.error_result (e)
    return result


def monitor_scene_show(id):
    obj = Monitor.objects.filter(id=id)
    for i in obj:
        print(i)
    return None



def add_scene(res1):
    try:
        for i in res1:
            Scene_monitor.objects.create (**i)
        res_dic = tools.success_result (None)
    except Exception as e:
        res_dic = tools.error_result (e)
    return res_dic


# 获得图标监控项的数据
def get_chart_data(id):
    datas = []
    data = TDGatherData.objects.filter (item_id=id)
    for d in data:
        temp = {
            'key': d.data_key,
            'values': d.data_value.split (',')
        }
        datas.append (temp)
    return datas


def get_basic_data(id):
    datas = {}
    data = TDGatherData.objects.filter (item_id=id)
    for d in data:
        datas[d.data_key] = d.data_value
    return datas


def getBySceneId(request, id):
    sm = Scene_monitor.objects.filter (scene_id=id)
    dic_data = []
    for s in model_to_dict (sm):
        itemId = s['item_id']
        monitor = Monitor.objects.get (id=itemId)
        item = model_to_dict (monitor)
        item['x'] = s['x']
        item['y'] = s['y']
        dic_data.append (item)
    print dic_data


def alternate_play_test(request):
    username = json.loads (request.body)
    res_list = get_scenes(username)
    return res_list

def alternate_play(request):
    # 获取当前用户
    username = get_active_user(request)['data']['bk_username']
    # 获取当前时间
    nowtime = datetime.datetime.now().strftime('%H:%M:%S')
    res_list = get_scenes(username,nowtime,nowtime)
    return  res_list


def get_scenes(user_name,start,end):
    """
    :param user_name: 用户名
    :param start: 轮播开始时间
    :param end: 轮播结束时间
    :return: 场景的参数
    """
    res_list = []
    scenes = []
    # 获取当前用户的岗位
    pos_id = Localuser.objects.get (user_name=user_name).user_pos_id
    # 获取岗位对应的场景
    scene = position_scene.objects.filter (position_id=pos_id)
    for x in scene:
        scenes.append (x.scene_id)
    # 遍历scenes,获取每个场景对应的监控项
    for i in scenes:
        # 初始化
        base_list = []
        chart_list = []
        flow_list = []
        job_list = []
        items_id = []
        # 场景对应的监控项id
        scene_monitor = Scene_monitor.objects.filter(scene_id = i)
        for k in scene_monitor:
            items_id.append(k.item_id)
        # 遍历场景的监控项ID
        for j in items_id:
            # 获取基本数据
            item = Monitor.objects.get (id=j)
            # 转成字典
            item_dict = model_to_dict (item)
            # 把时间类型转换为String
            item_dict['start_time'] = str (item.start_time)
            item_dict['end_time'] = str (item.end_time)
            item_dict['create_time'] = str (item.create_time)
            item_dict['edit_time'] = str (item.edit_time)
            #判断系统时间是否在轮播时间
            if start > str (item.start_time) and end < str (item.end_time):
                # 采集数据
                info = {
                    'id': item.id,
                    'params': item.params,
                    'gather_rule': item.gather_rule,
                    'gather_params': item.gather_params,
                }
                gather_data (**info)
                gather_rule = "select data_key,data_value,gather_error_log from td_gather_data where item_id = " + str (j)
                db = get_db ()
                cursor = db.cursor ()
                cursor.execute (gather_rule)
                results = cursor.fetchall ()
                dic = {}
                for i in results:
                    dic1 = {
                        i[0]: i[1],
                        'gather_status': i[2]
                    }
                    dic = dict (dic, **dic1)
                # 拼接监控项基础数据和采集数据
                item_dict = dict (item_dict, **dic)
                # 按不同的监控项类型保存
                if u'基本单元类型' == item.monitor_type:
                    base_list.append (item_dict)
                if u'图表单元类型' == item.monitor_type:
                    chart_list.append (item_dict)
                if u'流程单元类型' == item.monitor_type:
                    flow_list.append (item_dict)
                if u'作业单元类型' == item.monitor_type:
                    job_list.append (item_dict)
        data = {
            'base_list': base_list,
            'chart_list': chart_list,
            'flow_list': flow_list,
            'job_list': job_list,
        }
        res_list.append (data)
    return res_list
