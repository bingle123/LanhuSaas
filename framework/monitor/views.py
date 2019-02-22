# encoding:utf-8
import function
import tools
from common.mymako import render_json, render_mako_context
import json


# Create your views here.

def index(request):

    return render_mako_context(request, './monitor/show_message.html')


def index1(request):

    return render_mako_context(request, '123.html')


def unit_show(request):

    res = function.unit_show(request)
    return render_json(res)


def select_unit(request):

    res = function.select_unit(request)
    return render_json(res)


def edit_unit(request):

    res = function.edit_unit(request)
    return render_json(res)


def delete_unit(request):

    function.delete_unit(request)
    return render_json(None)


def add_unit(request):

    res = function.add_unit(request)
    return render_json(res)


def basic_test(request):
    res = function.basic_test(request)
    return render_json(res)


def job_test(request):
    res = function.job_test(request)
    return render_json(res)


def test1(request):
    res = function.ttt(request)
    return render_json(res)


def change_status(req):
    res=function.change_unit_status(req)
    return render_json(res)


def chart_get_test(request):
    """
    图表单元采集测试
    :param request:
    :return:
    """
    res = function.chart_get_test(request)
    return render_json(res)


def flow_change(request):
    """
    图表单元采集测试
    :param request:
    :return:
    """
    res = function.flow_change(request)
    return render_json(res)

def node_name(request):
    res = function.node_name(request)
    return render_json(res)

def start_flow_task(request):
    info=json.loads(request.body)
    res = tools.start_flow_task(**info)
    return render_json(res)

def node_state(request):
    res = function.node_state(request)
    return render_json(res)