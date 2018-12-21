# -*- coding: utf-8 -*-
from common.mymako import render_json
from common.mymako import render_mako_context
from shell_app import function


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


def show_host(request):
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


def user_carousel_setting(request):
    """
    用户设置
    :param request:
    :return:
    """
    result = function.user_carousel(request)
    return render_json(result)


def get_user_carousel_time(request):
    """
    获取用户Carousel设置轮播时间与轮播数量
    :param request:
    :return:
    """
    result = function.get_user_carousel_time(request)
    return render_json(result)


def get_scene_by_now_time(request):
    """
    获取场景信息
    :param request:
    :return:
    """
    result = function.get_scene_by_staff_position_id_time_order_by_scene_order_id(request)
    return render_json(result)


def position_setting_html(request):
    """
    岗位设置页面
    :param request:
    :return:
    """
    return render_mako_context(request, './shell_app/position_setting.html')


def get_json_test(request):
    """
    测试接口返回json专用
    :param request:
    :return:
    """
    temp_result = function.get_test_json(request)
    return render_json(temp_result)

