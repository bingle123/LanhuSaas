# encoding:utf-8
import function
import tools
from common.mymako import render_json, render_mako_context
import json


# Create your views here.
def index(request):
    """
    监控项目首页
    :param request:
    :return:
    """
    return render_mako_context(request, './monitor_item/show_message.html')


def unit_show(request):
    """
    显示函数
    :param request:
    :return:
    """
    res = function.unit_show(request)
    return render_json(res)


def select_unit(request):
    """
    查询函数
    :param request:
    :return:
    """
    res = function.select_unit(request)
    return render_json(res)


def edit_unit(request):
    """
    编辑函数
    :param request:
    :return:
    """
    res = function.edit_unit(request)
    return render_json(res)


def delete_unit(request):
    """
    删除函数
    :param request:
    :return:
    """
    function.delete_unit(request)
    return render_json(None)


def add_unit(request):
    """
    添加函数
    :param request:
    :return:
    """
    res = function.add_unit(request)
    return render_json(res)


def basic_test(request):
    """

    :param request:
    :return:
    """
    res = function.basic_test(request)
    return render_json(res)


def job_test(request):
    """
    作业采集测试函数
    :param request:
    :return:
    """
    res = function.job_test(request)
    return render_json(res)


def change_status(req):
    """

    :param req:
    :return:
    """
    res = function.change_unit_status(req)
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
    """

    :param request:
    :return:
    """
    res = function.node_name(request)
    return render_json(res)


def start_flow_task(request):
    """

    :param request:
    :return:
    """
    info = json.loads(request.body)
    print info
    res = tools.start_flow_task(**info)
    return render_json(res)


def node_state(request):
    """

    :param request:
    :return:
    """
    res = function.node_state(request)
    return render_json(res)


def resume_flow(req):
    """

    :param req:
    :return:
    """
    res = json.loads(req.body)
    item_id = res['item_id']
    name = res['name']
    rt = tools.resume_flow(item_id=item_id, name=name)
    return render_json(rt)


def node_state_by_item_id(request):
    """

    :param request:
    :return:
    """
    res = function.node_state_by_item_id(request)
    return render_json(res)
