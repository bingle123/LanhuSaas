# -*- coding: utf-8 -*-
from django.shortcuts import render
from common.mymako import render_json
from common.mymako import render_mako_context
from . import function
import json
import sys
from logmanagement.function import add_log,make_log_info,get_active_user


def show_index(request):
    """

    :param request:
    :return:
    """
    return render_mako_context(request, './notification/notification.html')


def select_all_rules(request):
    """

    :param request:
    :return:
    """
    alert_rules = function.select_all_rules()
    return render_json(alert_rules)


def select_rule(request):
    """

    :param request:
    :return:
    """
    rule_id = json.loads(request.body)
    selected_rule = function.select_rule(rule_id)
    return render_json(selected_rule)


def del_rule(request):
    """

    :param request:
    :return:
    """
    try:
        rule_id = json.loads(request.body)
        status = function.del_rule(rule_id)
        info = make_log_info(u'删除告警规则', u'业务日志', u'TbAlertRule', sys._getframe().f_code.co_name,
                         get_active_user(request)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'删除告警规则', u'业务日志', u'TbAlertRule', sys._getframe().f_code.co_name,
                         get_active_user(request)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return render_json(status)


def force_del_rule(request):
    """

    :param request:
    :return:
    """
    try:
        print request.body
        rule_id = json.loads(request.body)
        status = function.force_del_rule(rule_id)
        info = make_log_info(u'强制删除告警规则', u'业务日志', u'TbAlertRule', sys._getframe().f_code.co_name,
                         get_active_user(request)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'强制删除告警规则', u'业务日志', u'TbAlertRule', sys._getframe().f_code.co_name,
                         get_active_user(request)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return render_json(status)


def add_rule(request):
    """

    :param request:
    :return:
    """
    rule_data = json.loads(request.body)
    try:
        status = function.add_rule(rule_data)
        info = make_log_info(u'增加或更新告警规则', u'业务日志', u'TbAlertRule', sys._getframe().f_code.co_name,
                         get_active_user(request)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'增加或更新告警规则', u'业务日志', u'TbAlertRule', sys._getframe().f_code.co_name,
                         get_active_user(request)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return render_json(status)


def select_rules_pagination(request):
    """

    :param request:
    :return:
    """
    page_info = json.loads(request.body)
    selected_rules = function.select_rules_pagination(page_info)
    return render_json(selected_rules)