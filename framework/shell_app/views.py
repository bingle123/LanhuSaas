# -*- coding: utf-8 -*-
from common.mymako import render_json
from common.mymako import render_mako_context
from shell_app import function
import time


def add_scene(request):
    """
    增加场景表单HTML
    :param request:
    :return:
    """
    return render_mako_context(request, './shell_app/add_scene.html')


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


def position_setting_html(request):
    """
    岗位设置页面
    :param request:
    :return:
    """
    return render_mako_context(request, './shell_app/position_setting.html')


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
    print 111
    print request.body
    return render_json(function.get_scenes_all())


def get_json_test(request):
    """
    测试接口返回json专用
    :param request:
    :return:
    """
    temp_result = function.get_test_json(request)
    return render_json(temp_result)


