# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from blueking.component.shortcuts import get_client_by_request
from common.mymako import render_json
from common.mymako import render_mako_context
from common.log import logger
from  shell_app import function

def showselect(request):
    """
    选择服务器页面
    :param request:
    :return: 选择服务器页面
    """
    return render_mako_context(request, './common/select.html')

def show_Host(request):
    """
    主机页面展示，包含分页功能
    :param request: clickPage:页码数
    :return:        json
    """
    show_host = function.show_host(request)
    return render_json(show_host)


def modle_Tree_Host(request):
    """
    查询集群和模块
    :param request:
    :return: json
    """
    modle_tree_host = function.modle_tree_host(request)
    return render_json(modle_tree_host)

def select_Module_Host(request):
    """
    查询模块下面对应的主机(未完成)
    :param request:
    :return: json
    """
    select_module_host = function.select_module_host(request)
    return render_json (select_module_host)

