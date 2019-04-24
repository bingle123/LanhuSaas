# -*- coding: utf-8 -*-
import function
from common.mymako import render_json, render_mako_context
import json
from common.utils import get_current_time
from gather_data.function import gather_data_migrate,gather_data_save
from iqube_interface.views import gather_base_test


# Create your views here.

def index(request):
    """

    :param request:
    :return:
    """
    return render_mako_context(request, './monitor_scene/senceSet.html')


def demo(request):
    """

    :param request:
    :return:
    """
    return render_mako_context(request, './Demo.html')


def monitor_show(request):
    """

    :param request:
    :return:
    """
    res = function.monitor_show(request)
    return render_json(res)


def addSence(request):
    """

    :param request:
    :return:
    """
    res = function.addSence(request)
    return render_json(res)


def select_table(request):
    """

    :param request:
    :return:
    """
    res = function.select_table(request)
    return render_json(res)


def delete_scene(request):
    """

    :param request:
    :return:
    """
    res = function.delete_scene(request)
    return render_json(res)


def editSence(request):
    """

    :param request:
    :return:
    """
    res = function.editSence(request)
    return render_json(res)


def pos_name(request):
    """

    :param request:
    :return:
    """
    res = function.pos_name(request)
    return render_json(res)


def scene_data(request):
    """
    提取编排数据
    :param request:
    :return:
    """
    id = request.body
    res = function.scene_data(id)
    return render_json(res)


def paging(request):
    """
    场景编排初始化查询
    :param request:
    :return:
    """
    res = function.paging(request)
    return render_json(res)


def scene_show(request):
    """
    场景编排展示
    :param request:
    :return:
    """
    param = json.loads(request.body)
    res = function.scene_show(param)
    return render_json(res)


def monitor_scene_show(request):
    """

    :param request:
    :return:
    """
    id = request.body
    res = function.monitor_scene_show(id)
    return render_json(res)


def get_chart_data(req, id):
    """

    :param req:
    :param id:
    :return:
    """
    res = function.get_chart_data(id)
    return render_json(res)


def get_basic_data(req, id):
    """

    :param req:
    :param id:
    :return:
    """
    res = function.get_basic_data(id)
    print res;
    return render_json(res)


def getBySceneId(request, id):
    """

    :param request:
    :param id:
    :return:
    """
    res = function.getBySceneId(request, id)
    return render_json(res)


def alternate_play(request):
    """

    :param request:
    :return:
    """
    res = function.alternate_play(request)
    return render_json(res)


def alternate_play_test(request):
    res = function.alternate_play_test(request)
    return render_json(res)


def get_all_pos(request):
    res = function.get_all_pos(request)
    return render_json(res)


def get_scenes(request):
    res = function.get_scenes(request)
    return render_json(res)


# 场景颜色保存方法
def scene_color_save(request):
    scene_color = json.loads(request.body)
    status = function.scene_color_save(scene_color)
    return render_json(status)


# 根据场景ID获取场景颜色
def scene_color_get(request):
    color = function.scene_color_get(request.body)
    return render_json(color)


# 根据场景ID删除场景颜色
def scene_color_del(request):
    status = function.scene_color_del(request.body)
    return render_json(status)


def load_flow_graph(request):
    """
    :param request:
    :return:
    """
    return render_mako_context(request, './monitor_scene/load_flow_graph1.html')


def edit_flow_graph(request):
    """
    :param request:
    :return:
    """
    return render_mako_context(request, './monitor_scene/edit_flow_graph.html')


# 判断当前监控项是否需要采集
def is_monitor_item_collect(request):
    """
    获取唯一的数据库系统时间，用于判断当前监控项是否在采集时间区域
    :param request:
    :return:
    """
    # 将监控项信息转换为json格式
    monitor_item = json.loads(request.body);
    # 获取当前系统时间
    result = get_current_time()
    # 当前时间
    current_time = list(result[0])[0]
    # 开始时间
    start_time = monitor_item["start_time"]
    # 结束时间
    end_time = monitor_item["end_time"]

    # 如果当前时间在监控项的采集时间范围内，执行采集，调用一体化服务
    if (current_time >= start_time) and (current_time <= end_time):
        result = gather_base_test(request)
        # 历史数据迁移
        gather_data_migrate(monitor_item["id"])
        # print json.loads(result.content)["results"]
        info = {
            "type" : "add",
            "item_id" : monitor_item["id"],
            "measures" : json.loads(result.content)["results"]
        }
        print info
        # 采集数据入库
        gather_data_save(info)
        return result
    else :
        return render_json({"result": "1"})



def monitor_scene_fuzzy_search(request):
    """
    场景编排展示
    :param request:
    :return:
    """
    param = json.loads(request.body)
    res = function.monitor_scene_fuzzy_search(param)
    return render_json(res)