# -*- coding: utf-8 -*-
from common.mymako import render_json
from common.mymako import render_mako_context
from django.shortcuts import render
from . import function
import json
import tools


def data_base(request):
    """

    :param request:
    :return:
    """
    return render_mako_context(request, './main/database.html')


def position(request):
    """

    :param request:
    :return:
    """
    return render_mako_context(request, './position/position.html')


def index(request):
    """
    主页
    :param request:
    :return:
    """
    return render_mako_context(request, './main/maintenanceIndex.html')

# jlq-2019-05-07-add
def network_panorama(request):
    """
    页面1
    :param request:
    :return:
    """
    return render_mako_context(request, './main/networkPanorama.html')

# jlq-2019-05-08-add
def night_first(request):
    """
    页面1
    :param request:
    :return:
    """
    return render_mako_context(request, './main/nightFirst.html')



def scene_set(request):
    """

    :param request:
    :return:
    """
    return render_mako_context(request, './monitor_scene/senceSet.html')


def calendar(request):
    """

    :param request:
    :return:
    """
    return render_mako_context(request, './main/Calendar.html')


def main(request):
    """
    管理主页
    :param request:
    :return:
    """
    return render_mako_context(request, './common/main.html')


def scene_carousel(request):
    """
    vue-场景轮播暂时页面
    :param request:
    :return:
    """
    return render_mako_context(request, './scene/scenecarousel.html')


def scene_carousel_test(request):
    """
    vue-场景轮播暂时页面
    :param request:
    :return:
    """
    return render_mako_context(request, './scene/scenecarousel1.html')


def scene_list(request):
    """
    场景管理列表
    :param request:
    :return:
    """
    return render_mako_context(request, './shell_app/scene_list.html')


def carousel(request):
    """
    页面轮播效果
    :param request:
    :return:
    """
    return render_mako_context(request, './common/carousel.html')


def show_select(request):
    """
    选择服务器页面
    :param request:
    :return: 选择服务器页面
    """
    return render_mako_context(request, './common/select.html')


def ming(request):
    """

    :param request:
    :return:
    """
    return render_mako_context(request, './main/ming.html')


def select_host(request):
    """
    主机页面展示，包含分页功能
    :param request: clickPage:页码数
    :return:        json
    """
    host = function.show_host(request)
    return render_json(host)


def model_tree_host(request):
    """
    查询集群和模块
    :param request:
    :return: json
    """
    tree_host = function.model_tree_host(request)
    return render_json(tree_host)


def select_module_host(request):
    """
    查询模块下面对应的主机(未完成)
    :param request:
    :return: json
    """
    module_host = function.select_module_host(request)
    return render_json(module_host)


def get_scene_by_now_time(request):
    """
    获取场景信息
    :param request:
    :return:
    """
    result = function.get_scene_by_staff_position_id_time_order_by_scene_order_id(request)
    return render_json(result)


def get_staff_scene(request):
    """
    获取用户场景
    :param request:
    :return:
    """
    result = function.get_staff_scene(request)
    return render_json(result)


def get_positions_all(request):
    """
    获取所有岗位
    :param request:
    :return:
    """
    result = function.get_positions_all()
    return render_json(result)


def add_scene_form(request):
    """
    增加场景表单
    :param request:
    :return:
    """
    request_body = request.body
    print request_body
    if request_body is not None:
        body_json = json.loads(request_body)
        res = function.add_scene(body_json)
    else:
        res = None
    return render_json(res)


def get_json_test(request):
    """
    测试接口返回json专用
    :param request:
    :return:
    """
    temp_result = function.get_test_json(request)
    return render_json(temp_result)


def get_active_user(request):
    """
    通过蓝鲸获取当前用户
    :param request:
    :return:
    """
    res = tools.get_active_user(request)
    return render_json(res)


def get_guotai_system_info(request):
    """
    获取国泰系统系统状态
    :param request:
    :return:
    """
    res = function.get_guotai_system_info(request)
    return render_json(res)
def ywzl_panorama(request):
    """
    获取国泰系统系统状态
    :param request:
    :return:
    """
    return render_mako_context(request, './main/ywzlPanorama.html')
def trace_panorama(request):
    """
    获取国泰系统系统状态
    :param request:
    :return:
    """
    return render_mako_context(request, './main/tracePanorama.html')
