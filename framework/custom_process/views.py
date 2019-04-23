# -*- coding: utf-8 -*-
from common.mymako import render_json
from common.mymako import render_mako_context
from . import function
import json
import sys
from logmanagement.function import add_log, make_log_info, get_active_user


def show_index(request):
    """
    定制流程页面
    :param request:
    :return:
    """
    return render_mako_context(request, './custom_process/custom_process.html')


def select_all_nodes(request):
    """

    :param request:
    :return:
    """
    node_list = function.select_all_nodes()
    return render_json(node_list)


def add_node(request):
    """

    :param request:
    :return:
    """
    try:
        node = json.loads(request.body)
        status = function.add_node(node)
        info = make_log_info(u'增加或更新自定义流程', u'业务日志', u'TbCustProcess', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '成功', '无')
    except Exception as e:
        print e
        info = make_log_info(u'增加或更新自定义流程', u'业务日志', u'TbCustProcess', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return render_json(status)


def update_node_status(request):
    """

    :param request:
    :return:
    """
    node = json.loads(request.body)
    status = function.update_node_status(node)
    return render_json(status)


def change_status_flag(request):
    """

    :param request:
    :return:
    """
    node = json.loads(request.body)
    status = function.change_status_flag(node)
    return render_json(status)


def del_node(request):
    """

    :param request:
    :return:
    """
    try:
        node_id = json.loads(request.body)
        status = function.del_node(node_id)
        info = make_log_info(u'删除自定义流程', u'业务日志', u'TbCustProcess', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'删除自定义流程', u'业务日志', u'TbCustProcess', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return render_json(status)


def select_node(request):
    """

    :param request:
    :return:
    """
    node_id = json.loads(request.body)
    node_list = function.select_node(node_id)
    return render_json(node_list)


def truncate_node(request):
    """

    :param request:
    :return:
    """
    try:
        status = function.truncate_node()
        info = make_log_info(u'删除所有自定义流程', u'业务日志', u'TbCustProcess', sys._getframe().f_code.co_name,
                         get_active_user(request)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'删除所有自定义流程', u'业务日志', u'TbCustProcess', sys._getframe().f_code.co_name,
                         get_active_user(request)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return render_json(status)


def clear_execute_status(request):
    """

    :param request:
    :return:
    """
    status = function.clear_execute_status()
    return render_json(status)


def select_all_bkusers(request):
    """

    :param request:
    :return:
    """
    bk_users = function.select_all_bkusers()
    return render_json(bk_users)


def send_notification(request):
    """

    :param request:
    :return:
    """
    notification = json.loads(request.body)
    status = function.send_notification(notification)
    return render_json(status)


def select_nodes_pagination(request):
    """

    :param request:
    :return:
    """
    page_info = json.loads(request.body)
    selected_nodes = function.select_nodes_pagination(page_info)
    return render_json(selected_nodes)
