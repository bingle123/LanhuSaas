# encoding:utf-8
import function
import tools
from common.mymako import render_json, render_mako_context
import json


# Create your views here.
# 网页路由
def index(request):

    return render_mako_context(request, './monitor_item/show_message.html')


# 显示函数
def unit_show(request):

    res = function.unit_show(request)
    return render_json(res)


# 查询函数
def select_unit(request):

    res = function.select_unit(request)
    return render_json(res)


# 编辑函数
def edit_unit(request):

    res = function.edit_unit(request)
    return render_json(res)


# 删除函数
def delete_unit(request):

    function.delete_unit(request)
    return render_json(None)


# 添加函数
def add_unit(request):
    res = function.add_unit(request)

    return render_json(res)


def basic_test(request):
    res = function.basic_test(request)
    return render_json(res)


# 作业采集测试函数
def job_test(request):
    res = function.job_test(request)
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
    print info
    res = tools.start_flow_task(**info)
    return render_json(res)

def node_state(request):
    res = function.node_state(request)
    return render_json(res)

def resume_flow(req):
    res=json.loads(req.body)
    item_id=res['item_id']
    name=res['name']
    rt=tools.resume_flow(item_id=item_id,name=name)
    return render_json(rt)

def node_state_by_item_id(request):
    res = function.node_state_by_item_id(request)
    return render_json(res)