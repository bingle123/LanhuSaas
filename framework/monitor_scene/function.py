# -*- coding: utf-8 -*-
from __future__ import division
import json
import math
from django.forms import model_to_dict
from models import Scene
from models import SceneDesign
from models import SceneColor
from models import position_scene
from monitor_item.models import Monitor, Job, Scene_monitor
from monitor_item import tools
from gather_data.models import TDGatherData
import sys
from logmanagement.function import add_log, make_log_info, get_active_user
from datetime import datetime
import pytz
from position.models import *
from market_day.models import Area
from market_day.function import tran_time_china, tran_china_time_other, check_jobday
from django.db.models import Q
from xml.etree import ElementTree  #引入ElementTree的包
from monitor_item.models import *
from db_connection.function import get_db
def monitor_show(request):
    """
    渲染整个页面的数据
    :param request:
    :return:
    """
    # 搜索,按id倒排序
    monitor = Scene.objects.all()
    res_list = []
    for i in monitor:
        dic = {
            'id': i.id,
            'scene_name': i.scene_name,
            'scene_startTime': str(i.scene_startTime),
            'scene_endTime': str(i.scene_endTime),
            'scene_creator': i.scene_creator,
            'scene_creator_time': str(i.scene_creator_time),
            'scene_editor': i.scene_editor,
            'scene_editor_time': str(i.scene_editor_time),
            'pos_name': ''
        }
        position = position_scene.objects.filter(scene=i.id)
        for c in position:
            job = pos_info.objects.filter(id=c.position_id)
            for j in job:
                jobs = {
                    "pos_name": j.pos_name
                }
                dic['pos_name'] = jobs["pos_name"]
        res_list.append(dic)
    return res_list


def addSence(request):
    """

    :param request:
    :return:
    """
    id = None
    try:
        res = request.body
        senceModel = json.loads(res)
        print senceModel
        starttime = senceModel['data']["scene_startTime"]
        endtime = senceModel['data']["scene_endTime"]
        temp_date = datetime(2019, 1, 1, int(starttime.split(':')[0]), int(starttime.split(':')[-1]), 0)
        timezone = Area.objects.get(id=senceModel['data']['area']).timezone
        starthour, startmin = tran_time_china(temp_date, timezone=timezone)
        starttime = starthour + ":" + startmin
        temp_date = datetime(2019, 1, 1, int(endtime.split(':')[0]), int(endtime.split(':')[-1]), 0)
        endhour, endmin = tran_time_china(temp_date, timezone=timezone)
        endtime = endhour + ":" + endmin
        senceModel2 = {
            "scene_name": senceModel['data']['scene_name'],
            "scene_startTime": starttime,
            "scene_endTime": endtime,
            "scene_creator": "admin",
            "scene_area": senceModel['data']['area']
        }
        id = Scene.objects.create(**senceModel2)
        senceModel3 = {
            "scene": id,
            "position_id": senceModel['data']["pos_name"]
        }
        position_scene.objects.create(**senceModel3)
        # 新增场景再添加场景与监控项的对应关系，编辑时再添加这个关系
        """
        for i in senceModel['monitor_data']:
            monitor_data = {
                'scene_id': id.id,
                'item_id': int(i['item_id']),
                'x': int(i['x']),
                'y': int(i['y']),
                'scale': i['scale'],
                'score': int(i['score']),
                'order': int(i['order']),
                'next_item':int(i['next_item'])
            }
            Scene_monitor.objects.create(**monitor_data)
        """
        info = make_log_info(u'增加场景', u'业务日志', u'position_scene', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
    except Exception as e:
        info = make_log_info(u'增加场景', u'业务日志', u'position_scene', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
    add_log(info)
    return {'scene_id': id.id}


def select_table(request):
    """

    :param request:
    :return:
    """
    res = request.body
    res_list = []
    monitor = Scene.objects\
        .filter(Q(scene_name__contains=res)|Q(scene_creator__contains=res)).order_by("-id")
    for i in monitor:
        dic = {
            'id': i.id,
            'scene_name': i.scene_name,
            'scene_startTime': str(i.scene_startTime),
            'scene_endTime': str(i.scene_endTime),
            'scene_creator': i.scene_creator,
            'scene_creator_time': str(i.scene_creator_time),
            'scene_editor': i.scene_editor,
            'scene_editor_time': str(i.scene_editor_time),
        }
        position = position_scene.objects.filter(scene=i.id)
        for c in position:
            job = pos_info.objects.filter(id=c.position_id)
            for j in job:
                jobs = {
                    "pos_name": j.pos_name
                }
                dic['pos_name'] = jobs["pos_name"]
        res_list.append(dic)
        print res_list
    return res_list


def delete_scene(request):
    """

    :param request:
    :return:
    """
    try:
        Scene.objects.filter(id=request.body).delete()
        Scene_monitor.objects.filter(scene_id=request.body).delete()
        info = make_log_info(u'删除场景', u'业务日志', u'position_scene', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
        add_log(info)
        position_scene.objects.filter(scene=request.body).delete()
        info = make_log_info(u'删除场景编排数据', u'业务日志', u'position_scene', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
        add_log(info)
    except Exception as e:
        info = make_log_info(u'删除场景', u'业务日志', u'position_scene', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
        add_log(info)
        info = make_log_info(u'删除场景', u'业务日志', u'position_scene', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
        add_log(info)
    return ""


def editSence(request):
    """

    :param request:
    :return:
    """
    try:
        model = json.loads(request.body)
        starttime = model['data']["scene_startTime"]
        endtime = model['data']["scene_endTime"]
        temp_date = datetime(2019, 1, 1, int(starttime.split(':')[0]), int(starttime.split(':')[-1]), 0)
        timezone = Area.objects.get(id=model['data']['area']).timezone
        starthour, startmin = tran_time_china(temp_date, timezone=timezone)
        starttime = starthour + ":" + startmin
        temp_date = datetime(2019, 1, 1, int(endtime.split(':')[0]), int(endtime.split(':')[-1]), 0)
        endhour, endmin = tran_time_china(temp_date, timezone=timezone)
        endtime = endhour + ":" + endmin
        senceModel2 = {
            "scene_name": model['data']['scene_name'],
            "scene_startTime": starttime,
            "scene_endTime": endtime,
            "scene_editor": "admin",
            "scene_area": model['data']['area']
        }
        Scene.objects.filter(id=model['data']['id']).update(**senceModel2)
        info = make_log_info(u'编辑场景', u'业务日志', u'Scene', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
        add_log(info)
        Scene_monitor.objects.filter(scene_id=model['data']['id']).delete()
        for i in model['monitor_data']:
            monitor_data = {
                'scene_id': model['data']['id'],
                'item_id': int(i['item_id']),
                'x': int(i['x']),
                'y': int(i['y']),
                'scale': i['scale'],
                'score': int(i['score']),
                'order': int(i['order']),
                'next_item': int(i['next_item'])
            }
            Scene_monitor.objects.create(**monitor_data)
            info = make_log_info(u'场景编排', u'业务日志', u'Scene', sys._getframe().f_code.co_name,
                                 request.user.username, '成功', '无')
            add_log(info)
            scene = Scene.objects.get(id=model['data']['id'])
            scene.save()
            job = pos_info.objects.filter(pos_name=model['data']["pos_name"])
        for j in job:
            senceModel3 = {
                "scene_id": model['data']['id'],
                "position_id": j.id
            }
        position_scene.objects.filter(scene=senceModel3['scene_id']).update(**senceModel3)
        info2 = make_log_info(u'编辑场景', u'业务日志', u'position_scene', sys._getframe().f_code.co_name,
                              request.user.username, '成功', '无')
        add_log(info2)
    except Exception as e:
        info = make_log_info(u'编辑场景', u'业务日志', u'Scene', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
        add_log(info)
        info2 = make_log_info(u'场景编排', u'业务日志', u'Monitor', sys._getframe().f_code.co_name,
                              request.user.username, '失败', repr(e))
        add_log(info2)
    return None


def scene_data(id):
    """

    :param id:
    :return:
    """
    try:
        obj = Scene_monitor.objects.filter(scene_id=id)
        data_list = []
        for scene_obj in obj:
            data_dic = model_to_dict(scene_obj)
            data_dic['scale'] = str(scene_obj.scale)
            monitor_data = Monitor.objects.filter(id=data_dic['item_id'])
            for monitor_item_obj in monitor_data:
                # 监控项采集表中只有一条记录
                gather_data = TDGatherData.objects.filter(item_id=monitor_item_obj.id)
                for gather_data_obj in gather_data:
                    data_dic['data_value'] = gather_data_obj.data_value
                data_dic['monitor_name'] = monitor_item_obj.monitor_name
                data_dic['monitor_type'] = monitor_item_obj.monitor_type
                data_dic['jion_id'] = monitor_item_obj.jion_id
                data_dic['gather_rule'] = monitor_item_obj.gather_rule
                data_dic['gather_params'] = monitor_item_obj.gather_params
                data_dic['params'] = monitor_item_obj.params
                data_dic['width'] = monitor_item_obj.width
                data_dic['height'] = monitor_item_obj.height
                data_dic['font_size'] = monitor_item_obj.font_size
                data_dic['period'] = monitor_item_obj.period
                data_dic['start_time'] = str(monitor_item_obj.start_time)
                data_dic['end_time'] = str(monitor_item_obj.end_time)
                data_dic['creator'] = monitor_item_obj.creator
                data_dic['editor'] = monitor_item_obj.editor
                data_dic['status'] = monitor_item_obj.status
                data_dic['contents'] = monitor_item_obj.contents
                data_dic['monitor_area'] = monitor_item_obj.monitor_area
                data_dic['source_type'] = monitor_item_obj.source_type
                data_dic['target_name'] = monitor_item_obj.target_name
                data_dic['measure_name'] = monitor_item_obj.measure_name
                data_dic['dimension'] = monitor_item_obj.dimension
                data_dic['display_type'] = monitor_item_obj.display_type
                data_dic['display_rule'] = monitor_item_obj.display_rule
            data_list.append(data_dic)
        res = tools.success_result(data_list)
    except Exception as e:
        res = tools.error_result(e)
    return res


def pos_name(request):
    """

    :param request:
    :return:
    """
    job = pos_info.objects.all()
    res_list = []
    for i in job:
        dic = {
            'id': i.id,
            'pos_name': i.pos_name
        }
        res_list.append(dic)
    return res_list

# 初始化场景查询方法
def paging(request):
    """

    :param request:
    :return: 返回当前页的创建信息
    """
    res = json.loads(request.body)
    page = res['page']
    limit = res['limit']
    start_page = limit * page - 9
    # 根据id倒排序
    # monitor = Scene.objects.all().order_by("-id")[start_page - 1:start_page + 9]
    # monitor2 = Scene.objects.all().values('id')
    # page_count = math.ceil(len(monitor2) / 10)
    # res_list = []
    # for i in monitor:
    #     starttime = tran_china_time_other(i.scene_startTime, i.scene_area)
    #     endtime = tran_china_time_other(i.scene_endTime, i.scene_area)
    #     dic = {
    #         'id': i.id,
    #         'scene_name': i.scene_name,
    #         'scene_startTime': str(starttime),
    #         'scene_endTime': str(endtime),
    #         'scene_creator': i.scene_creator,
    #         'scene_creator_time': str(i.scene_creator_time),
    #         'scene_editor': i.scene_editor,
    #         'scene_editor_time': str(i.scene_editor_time),
    #         'scene_area': i.scene_area,
    #         'scene_content':i.scene_content,
    #         'pos_name': '',
    #         'page_count': page_count,
    #     }
    #     position = position_scene.objects.filter(scene=i.id)
    #     for c in position:
    #         job = pos_info.objects.filter(id=c.position_id)
    #         for j in job:
    #             jobs = {
    #                 "pos_name": j.pos_name
    #             }
    #             dic['pos_name'] = jobs["pos_name"]
    #     res_list.append(dic)

    #20190516 彭英杰 start
    total = Scene.objects.all().count()
    sql_str ="SELECT a.id,a.scene_name,a.scene_startTime,a.scene_endTime,a.scene_creator,"\
             "a.scene_creator_time,a.scene_editor,a.scene_creator_time,a.scene_area "\
             ",a.scene_content,c.pos_name FROM"\
             " tb_monitor_scene a LEFT JOIN "\
             " tl_position_scene b on a.id = b.scene_id"\
            " LEFT JOIN tb_pos_info c ON b.position_id=c.id   "
    page_start = (page-1)*limit
    sql_str=sql_str+" LIMIT "+str(page_start)+","+str(limit)
    db = get_db()
    cursor = db.cursor()
    cursor.execute(sql_str)
    res = cursor.fetchall()
    cursor.close()
    res_list=[]
    if len(res)>0:
        page_count = math.ceil(total / 10)
        for obj in res:
            dic = {
                    'id': obj[0],
                    'scene_name': obj[1],
                    'scene_startTime': str(obj[2]),
                    'scene_endTime': str(obj[3]),
                    'scene_creator': obj[4],
                    'scene_creator_time': str(obj[5]),
                    'scene_editor': obj[6],
                    'scene_editor_time': str(obj[7]),
                    'scene_area': obj[8],
                    'scene_content':obj[9],
                    'pos_name': obj[10],
                    'page_count': page_count,
                }
            res_list.append(dic)

    #20190516 彭英杰 end
    return res_list


# 场景编排区域显示的四类监控项
def scene_show(res):
    """
    场景编排显示

    :param res:
    :return:
    """
    try:
        type = res['type']
        limit = res['limit']
        page = res['page']
        if type == 0:
            # 四类监控项全部按id倒排序（基本监控项与一体化基本监控项放一起）
            base_unit = Monitor.objects.filter(Q(monitor_type = 1) | Q(monitor_type= 5)).order_by("-id")
            base_page_data, base_page_count = tools.page_paging(base_unit, limit, page)
            # 四类监控项全部按id倒排序（图表监控项）
            chart_unit = Monitor.objects.filter(monitor_type='2').order_by("-id")
            chart_page_data, chart_page_count = tools.page_paging(chart_unit, limit, page)
            # 四类监控项全部按id倒排序（作业监控项）
            job_unit = Monitor.objects.filter(monitor_type='3').order_by("-id")
            job_page_data, job_page_count = tools.page_paging(job_unit, limit, page)
            # 四类监控项全部按id倒排序（流程监控项）
            flow_unit = Monitor.objects.filter(monitor_type='4').order_by("-id")
            flow_page_data, flow_page_count = tools.page_paging(flow_unit, limit, page)
            base_list = tools.obt_dic(base_page_data, base_page_count)
            chart_list = tools.obt_dic(chart_page_data, chart_page_count)
            job_list = tools.obt_dic(job_page_data, job_page_count)
            flow_list = tools.obt_dic(flow_page_data, flow_page_count)
            res_dic = {
                'base_list': base_list,
                'chart_list': chart_list,
                'job_list': job_list,
                'flow_list': flow_list,
            }
        # 基本监控项与一体化基本监控项
        elif type == 1:
            base_unit = Monitor.objects.filter(Q(monitor_type=1) | Q(monitor_type=5)).order_by("-id")
            base_page_data, base_page_count = tools.page_paging(base_unit, limit, page)
            base_list = tools.obt_dic(base_page_data, base_page_count)
            res_dic = {
                'base_list': base_list,
            }
        # 图表监控项
        elif type == 2:
            chart_unit = Monitor.objects.filter(monitor_type='2').order_by("-id")
            chart_page_data, chart_page_count = tools.page_paging(chart_unit, limit, page)
            chart_list = tools.obt_dic(chart_page_data, chart_page_count)
            res_dic = {
                'chart_list': chart_list,
            }
        # 作业监控项
        elif type == 3:
            job_unit = Monitor.objects.filter(monitor_type='3').order_by("-id")
            job_page_data, job_page_count = tools.page_paging(job_unit, limit, page)
            job_list = tools.obt_dic(job_page_data, job_page_count)
            job_status_list = []
            for i in job_list:
                try:
                    job_status = Job.objects.filter(job_id=i['jion_id']).last().status
                except Exception as e:
                    job_status = 0
                job_status_list.append(job_status)
            for i in range(0, len(job_status_list)):
                job_list[i]['job_status'] = job_status_list[i]
            res_dic = {
                'job_list': job_list,
            }
        # 流程监控项
        elif type == 4:
            flow_unit = Monitor.objects.filter(monitor_type='4').order_by("-id")
            flow_page_data, flow_page_count = tools.page_paging(flow_unit, limit, page)
            flow_list = tools.obt_dic(flow_page_data, flow_page_count)
            res_dic = {
                'flow_list': flow_list,
            }
        result = tools.success_result(res_dic)
    except Exception as e:
        result = tools.error_result(e)
    return result


def monitor_scene_show(id):
    """

    :param id:
    :return:
    """
    obj = Monitor.objects.filter(id=id).order_by("-id")
    data_list = []
    for i in obj:
        x = model_to_dict(i)
        x['edit_time'] = str(i.edit_time)
        x['create_time'] = str(i.create_time)
        x['start_time'] = str(i.start_time)
        x['end_time'] = str(i.end_time)
        # if x['monitor_type'] == u'作业单元类型':
        #     try:
        #         job_status = Job.objects.filter (job_id=i['jion_id']).last().status
        #     except Exception as e:
        #         job_status = 0
        # else:
        job_status = 0
        # print(job_status)
        x['job_status'] = job_status
        data_list.append(x)
    res = tools.success_result(data_list)
    return res


def add_scene(res1):
    """

    :param res1:
    :return:
    """
    try:
        for i in res1:
            Scene_monitor.objects.create(**i)
        res_dic = tools.success_result(None)
    except Exception as e:
        res_dic = tools.error_result(e)
        return res_dic


# 取得图表监控项采集数据
def get_chart_data(id):
    """
    获得图标监控项的数据
    :param id:
    :return:
    """
    datas = []
    data = TDGatherData.objects.filter(item_id=id)
    for d in data:
        if d.data_key != 'DB_CONNECTION':
            temp = {
                'key': d.data_key,
                'values': d.data_value.split(',')
            }
            datas.append(temp)
    return datas


# 取得基本监控项采集数据
def get_basic_data(id):
    """

    :param id:
    :return:
    """
    datas = {}
    data = TDGatherData.objects.filter(item_id=id)
    for d in data:
        datas[d.data_key] = d.data_value
    return datas


def getBySceneId(request, id):
    """

    :param request:
    :param id:
    :return:
    """
    sm = Scene_monitor.objects.filter(scene_id=id)
    dic_data = []
    print id
    for s in sm:
        scene_monitor = model_to_dict(s)
        itemId = scene_monitor['item_id']
        monitor = Monitor.objects.get(id=itemId)

        item = model_to_dict(monitor)
        item['start_time'] = str(item['start_time'])
        item['end_time'] = str(item['end_time'])
        item['x'] = scene_monitor['x']
        item['y'] = scene_monitor['y']
        dic_data.append(item)
    return tools.success_result(dic_data)


def alternate_play_test(request):
    """
    轮播测试
    :param request:
    :return:
    """
    res = json.loads(request.body)
    # 接收参数
    pos_id = res['pos_id']
    start = res['start']
    end = res['end']
    res_list = get_scenes(pos_id, start, end)
    return res_list


def query_pos_scene(request):
    '''
    场景
    :param request:
    :return:
    '''
    #res = json.loads(request.body)
    # 接收参数
    pos_id = request.POST.get('pos_id')
    start = request.POST.get('start')
    end = request.POST.get('end')
  #  scenes = []
    # 获取岗位对应的场景
    position_scenes = position_scene.objects.filter(position_id=pos_id)

    #for pos_scene in position_scenes:
    #    scenes.append(pos_scene.scene_id)

    scene_id_list = []
    for scene in position_scenes:
        # 场景
        temp_scene_dt = Scene.objects.filter(id=scene.scene_id,scene_content__isnull=False)
        if temp_scene_dt.count() == 0:
            continue
        temp_scene = temp_scene_dt.get()
        if start != None:
           if str(temp_scene.scene_startTime) <= end and str(temp_scene.scene_endTime) >= start:
              scene_id_list.append(scene.scene_id)
        else:
            scene_id_list.append(scene.scene_id)
    return scene_id_list


def query_curr_user_scene(request):
    user_dto = user_info.objects.filter(user_name=request.user.username)
    if user_dto.count() > 0:
        user_data = user_dto.get()
        pos_id = user_data.user_pos_id
        request.POST["pos_id"] = pos_id
        return query_pos_scene(request)
    else:
        return None


def alternate_play(request):
    """
    大屏轮播
    :param request:
    :return:
    """
    # 获取当前用户
    username = get_active_user(request)['data']['bk_username']
    # 获取当前用户的岗位id
    pos_id = user_info.objects.get(user_name=username).user_pos_id
    # 获取当前时间
    # nowtime = datetime.datetime.now().strftime('%H:%M:%S')
    res_list = get_scenes(pos_id, '', '')
    return res_list


def get_scenes(pos_id, start, end):
    """
    获取轮播页面
    :param position: 岗位名id
    :param start: 轮播开始时间
    :param end: 轮播结束时间
    :return: 场景的参数
    """
    res_list = []
    scenes = []
    # 获取岗位对应的场景
    position_scenes = position_scene.objects.filter(position_id=pos_id)
    # 判断是否为轮播测试；false就是测试
    is_alternate_test = False
    if start == '' and end == '':
        is_alternate_test = True
    for pos_scene in position_scenes:
        scenes.append(pos_scene.scene_id)
    # 遍历scenes,获取每个场景对应的监控项
    for scene in scenes:
        # 场景
        temp_scene = Scene.objects.get(id=scene)
        #
        flag = True
        if is_alternate_test:
            id = temp_scene.scene_area
            timezone = Area.objects.get(id=id).timezone
            tz = pytz.timezone(timezone)
            end = datetime.now(tz).strftime('%H:%M:%S')
            start = end
            flag = check_jobday(id)
        # 判断系统时间是否在轮播时间
        if str(temp_scene.scene_startTime) <= end and str(temp_scene.scene_endTime) >= start and flag == True:
            # 初始化
            base_list = []
            chart_list = []
            flow_list = []
            job_list = []
            temp_list = []
            scene_monitor_ids = []
            # 场景对应的监控项id
            scene_monitors = Scene_monitor.objects.filter(scene_id=scene)
            for scene_mon in scene_monitors:
                # items_id.append(k.item_id)
                scene_monitor_ids.append(scene_mon.id)
            # 遍历场景的场景—监控项ID
            for scene_mon_id in scene_monitor_ids:
                item_id = Scene_monitor.objects.get(id=scene_mon_id).item_id
                # 获取基本数据
                item = Monitor.objects.get(id=item_id)
                print item
                # 转成字典
                item_dict = model_to_dict(item)
                gather_data = TDGatherData.objects.filter(item_id=item_id)
                for gather_data_obj in gather_data:
                    item_dict["data_value"] = gather_data_obj.data_value
                # 把时间类型转换为String
                item_dict['start_time'] = str(item.start_time)
                item_dict['end_time'] = str(item.end_time)
                item_dict['create_time'] = str(item.create_time)
                item_dict['edit_time'] = str(item.edit_time)
                # 采集数据
                # info = {
                #     'id': item.id,
                #     'params': item.params,
                #     'gather_rule': item.gather_rule,
                #     'gather_params': item.gather_params,
                # }
                # gather_data (**info)
                # gather_rule = "select data_key,data_value,gather_error_log from td_gather_data where item_id = " + str (item_id)
                # db = get_db ()
                # cursor = db.cursor ()
                # cursor.execute (gather_rule)
                # results = cursor.fetchall ()
                # dic = {}
                # for i in results:
                #     dic1 = {
                #         i[0]: i[1],
                #         'gather_status': i[2]
                #     }
                #     dic = dict (dic, **dic1)
                # # 拼接监控项基础数据和采集数据
                # item_dict = dict (item_dict, **dic)
                # 拼接tl_scene_monitor信息
                scene_monitor = Scene_monitor.objects.get(id=scene_mon_id)
                scene_monitor_dict = {
                    'x': scene_monitor.x,
                    'y': scene_monitor.y,
                    'scale': str(scene_monitor.scale),
                    'score': scene_monitor.score,
                    'order': scene_monitor.order,
                }
                item_dict = dict(item_dict, **scene_monitor_dict)
                # 按不同的监控项类型保存
                if 1 == item.monitor_type or 5 == item.monitor_type:
                    base_list.append(item_dict)
                if 2 == item.monitor_type:
                    chart_list.append(item_dict)
                if 4 == item.monitor_type:
                    flow_list.append(item_dict)
                if 3 == item.monitor_type:
                    print item.jion_id
                    jobs = Job.objects.filter(job_id=item.jion_id)
                    status = jobs.last().status
                    temp_dict = {
                        'job_status': status
                    }
                    item_dict = dict(item_dict, **temp_dict)
                    job_list.append(item_dict)
            data = {
                'base_list': base_list,
                'chart_list': chart_list,
                'flow_list': flow_list,
                'job_list': job_list,
            }
            temp_list.append(data)
            scene_dict = {
                'scene_id': scene,
                'scene_content': temp_list
            }
            res_list.append(scene_dict)
    return res_list


def get_all_pos(request):
    """

    :param request:
    :return:
    """
    res = []
    positions = pos_info.objects.all()
    for i in positions:
        dict = {
            'id': i.id,
            'pos_name': i.pos_name
        }
        res.append(dict)
    return res


# 场景颜色保存方法
def scene_color_save(scene_color_info):
    print scene_color_info
    if 'add' == scene_color_info['type']:
        del scene_color_info['type']
        SceneColor.objects.create(**scene_color_info)
    elif 'edit' == scene_color_info['type']:
        del scene_color_info['type']
        SceneColor.objects.filter(scene_id=scene_color_info['scene_id']).update(**scene_color_info)
    else:
        raise RuntimeError('添加类型错误！')


# 根据场景ID获取场景颜色
def scene_color_get(scene_id):
    color_dict = dict()
    color = SceneColor.objects.get(scene_id=scene_id)
    color_dict['color'] = color.scene_color
    return color_dict


# 根据场景ID删除场景颜色
def scene_color_del(scene_id):
    color_dict = dict()
    SceneColor.objects.filter(scene_id=scene_id).delete()
    color_dict['status'] = "ok"
    return color_dict


# 场景编排模糊检索监控项
def monitor_scene_fuzzy_search(data):
    if 'basic' == data['type']:
        base_unit = Monitor.objects.filter(Q(monitor_type=1) | Q(monitor_type=5)).filter(monitor_name__contains=data['condition']).order_by("-id")
        base_page_data, base_page_count = tools.page_paging(base_unit, data['limit'], data['page'])
        base_list = tools.obt_dic(base_page_data, base_page_count)
        res_dic = {
            'base_list': base_list,
        }
        result = tools.success_result(res_dic)
    return result


def save_scene_design(data):
    """
    保存场景设计
    :param data:
    :return:
    """
    scene_design = {
        'scene_name': data['filename'],
        'scene_content': data['xml']
    }
    # 首先查询场景名称是否存在，存在就是编辑，不存在就提示名称错误
    scene_result = Scene.objects.filter(scene_name = data['filename'])
    print scene_result.__len__()
    if scene_result.__len__() == 0:
        # scene_obj = SceneDesign.objects.create(**scene_design)
        return {'id': "0"}
    else:
        Scene.objects.filter(id=str(scene_result[0].id)).update(**scene_design)
        get_scene_find_xml(int(scene_result[0].id))
        return {'id': "1"}


def query_scene_design(request):
    """
    分页查询所有已经设计保存的场景信息
    :param request:
    :return:
    """
    res = json.loads(request.body)
    #  个数
    limit = res['limit']
    #  当前页面号
    page = res['page']
    # 按id倒排序
    unit = SceneDesign.objects.all().order_by('-id')
    # 进入分页函数进行分页，返回总页数和当前页数据
    page_data, base_page_count = tools.page_paging(unit, limit, page)
    #  把返回的数据对象转为list
    res_list = tools.common_obt_dic(page_data, base_page_count)
    res_dic = {
        'scene_list': res_list,
    }
    return tools.success_result(res_dic)


def get_scene_find_xml(scene_id):
    '''
    根据场景id解析xml,
    新增到
    :param scene_id:
    :return:
    '''
    dto = Scene.objects.filter(id=scene_id).get()
    roota=ElementTree.XML(dto.scene_content)
    parent = roota.find("root", "mxGraphModel")
    list = parent._children
    for dto in list:
        if dto.tag == "object":
            dto_item_id = str(dto.attrib.get("item_id"))
            # 当关联监控项id为null或为空串就直接进入下一个循环
            if dto_item_id is None or dto_item_id is "":
                continue
            int_item_id = int(dto_item_id)
            temp_dto = Scene_monitor.objects.filter(scene_id=scene_id,item_id= int_item_id)
            if temp_dto.count() == 0:
                # 只有等于零时才新增
                scene_dto = Scene_monitor()
                scene_dto.item_id = int_item_id
                scene_dto.scene_id = scene_id
                scene_dto.x = 0
                scene_dto.y = 0
                scene_dto.scale = 0.0
                scene_dto.score = 0
                scene_dto.order = 0
                scene_dto.save()
                print "场景 "+str(scene_id)+" "+dto_item_id+"保存成功"
            else:
                print "场景 " + str(scene_id) + " " + dto_item_id + "已存在，不处理"


def page_query_scene(request):
    """
    分页查询场景
    :param request:
    :return:
    """
    res = json.loads(request.body)
    res_content = res['data']
    #  个数
    limit = res['limit']
    #  当前页面号
    page = res['page']
    # 按id倒排序
    if res_content != "":
        unit = Scene.objects.filter(Q(scene_name__icontains=res_content)).order_by("-id")
    else:
        unit = Scene.objects.all().order_by('-id')
    # 进入分页函数进行分页，返回总页数和当前页数据
    page_data, base_page_count = tools.page_paging(unit, limit, page)
    res_list = [];
    for scene_obj in page_data:
        starttime = tran_china_time_other(scene_obj.scene_startTime, scene_obj.scene_area)
        endtime = tran_china_time_other(scene_obj.scene_endTime, scene_obj.scene_area)

        dic = {
            'id': scene_obj.id,
            'scene_name': scene_obj.scene_name,
            'scene_startTime': str(starttime),
            'scene_endTime': str(endtime),
            'scene_creator': scene_obj.scene_creator,
            'scene_creator_time': str(scene_obj.scene_creator_time),
            'scene_editor': scene_obj.scene_editor,
            'scene_editor_time': str(scene_obj.scene_editor_time),
            'scene_area': scene_obj.scene_area,
            'scene_content':scene_obj.scene_content,
            'page_count': base_page_count,
        }
        res_list.append(dic)
    res_dic = {
        'scene_list': res_list,
    }
    return tools.success_result(res_dic)

def page_query_xml_show(id):
    dto = Scene.objects.filter(id=id)
    if dto.count() > 0:
        return dto.get().scene_content
    else:
        return None

def query_scene_item_data_handle(list_id):
    arr = []
    item_ids = [] #所有id
    for dto_item_id in list_id:
        if  dto_item_id.isdigit():  # 验证是否为数字
            item_ids.append(dto_item_id)
    list_dto_item = Monitor.objects.filter(id__in=item_ids)
    list_dto_gather = TDGatherData.objects.filter(item_id__in=item_ids)
    arr_dto_dt ={}
    for dto_temp in list_dto_gather:
        arr_dto_dt[dto_temp.item_id] = dto_temp
    for dto_item in list_dto_item:
        dt = {}
        dt["id"] = dto_item.id # 监控项表  id
        gather_dto = arr_dto_dt.get(dto_item.id) #采集表
        str = None
        if gather_dto != None:
            str = gather_dto.data_value
        if str != None and dto_item.target_name != None \
                                    and dto_item.measure_name != None:
             if str.find("[{") == 0:
                 json_dto = json.loads(str)
                 key = dto_item.target_name + "_" + dto_item.measure_name
                 txt = json_dto[0].get(key)
             elif gather_dto.data_key.upper().find("_CONNECTION")>-1\
                     and dto_item.contents != None and dto_item.contents !="":
                 txt = "@" + dto_item.contents
             if  'txt' not in locals().keys() or txt == None :
                 txt = "@" + dto_item.monitor_name
             dt["key_val"] = txt
        else:
            if gather_dto.data_key.upper().find("_CONNECTION")>-1 \
                     and dto_item.contents != None and dto_item.contents !="":
                dt["key_val"] = "@"+dto_item.contents
            else:
                dt["key_val"] = "@" + dto_item.monitor_name
        if 'key' in locals().keys():
            dt["key"] = key
        else:
            dt["key"] =""
            dt["key_name"] = dto_item.display_rule#.decode("utf-8")

            dt["item_type"] = dto_item.monitor_type
        arr.append(dt)

    # for dto_item_id in list_id:
    #     if not dto_item_id.isdigit(): # 验证是否为数字
    #         continue
    #     item_id = int(dto_item_id)
    #     item_dto = Monitor.objects.filter(id=item_id)
    #     if item_dto.count()>0:
    #         item_vo = item_dto.get()
    #         gather_data = TDGatherData.objects.filter(item_id=item_id)
    #         if gather_data.count()>0:
    #             if gather_data.count() >1:
    #                 gather_dto=gather_data.all()[0]
    #             else:
    #                 gather_dto = gather_data.get()
    #             dt = {}
    #             dt["id"] = dto_item_id
    #             str = gather_dto.data_value
    #             if str !=None and item_vo.target_name != None\
    #                     and item_vo.measure_name != None:
    #                 if str.find("[{") == 0:
    #                     json_dto = json.loads(str)
    #                     key = item_vo.target_name + "_" + item_vo.measure_name
    #                     txt = json_dto[0].get(key)
    #                 if  'txt' not in locals().keys() or txt == None :
    #                     txt = "@" + item_vo.monitor_name
    #                 dt["key_val"] = txt
    #             else:
    #                 dt["key_val"] = "@" + item_vo.monitor_name
    #             if 'key' in locals().keys():
    #                 dt["key"] = key
    #             else:
    #                 dt["key"] =""
    #             dt["key_name"] = item_vo.display_rule#.decode("utf-8")
    #
    #             dt["item_type"] = item_vo.monitor_type
    #             arr.append(dt)
        #TDGatherData
    return  arr