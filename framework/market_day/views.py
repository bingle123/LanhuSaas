# -*- coding:utf-8 -*-
from shell_app.function import render_json
import function
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import tasks
import sys
from logmanagement.function import add_log, make_log_info, get_active_user


def get_holiday(request, area):
    """

    :param request:
    :param area:
    :return:
    """
    days = function.get_holiday(request, area)
    return render_json(days)


@csrf_exempt
def get_file(request, area):
    """

    :param request:
    :param area:
    :return:
    """
    path = function.get_file(request, area)
    return HttpResponse('ok')


def send_demo(request, email):
    """

    :param request:
    :param email:
    :return:
    """
    print email
    tasks.sendemail.delay(email)
    return HttpResponse('success')


def delall(request, area):
    """

    :param request:
    :param area:
    :return:
    """
    try:
        flag = function.delall(area)
        info = make_log_info(u'删除全部交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
    except Exception as e:
        info = make_log_info(u'删除全部交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
    add_log(info)
    return render_json(flag)


def delone(request):
    """

    :param request:
    :return:
    """
    try:
        function.delone(request)
        info = make_log_info(u'变更为交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
    except Exception as e:
        info = make_log_info(u'变更为交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
    add_log(info)
    return render_json('ok')


def addone(request):
    """

    :param request:
    :return:
    """
    try:
        function.addone(request)
        info = make_log_info(u'取消交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
    except Exception as e:
        info = make_log_info(u'取消交易日', u'业务日志', u'Holiday', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
    add_log(info)
    return render_json('ok')


def get_all_timezone(request):
    """

    :param request:
    :return:
    """
    res = function.get_all_timezone()
    return render_json(res)


def get_data_header(request):
    """

    :param request:
    :return:
    """
    function.get_header_data(request)
    return HttpResponse('ok')


def add_area(request):
    """

    :param request:
    :return:
    """
    res = function.add_area(request)
    return render_json(res)


def get_all_area(request):
    """

    :param request:
    :return:
    """
    res = function.get_all_area(request)
    return render_json(res)


def del_area(request, name):
    """

    :param request:
    :param name:
    :return:
    """
    res = function.del_area(name)
    return render_json(res)


def test(request):
    """

    :param request:
    :return:
    """
    # 测试专用view
    res = function.check_jobday(1)
    return render_json(res)
