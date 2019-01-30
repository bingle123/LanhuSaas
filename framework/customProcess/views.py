# -*- coding: utf-8 -*-
from django.shortcuts import render
from common.mymako import render_json
from common.mymako import render_mako_context
from . import function
import json


def show_index(request):
    return render_mako_context(request, './customProcess/customProcess.html')


def select_all_nodes(request):
    node_list = function.select_all_nodes()
    return render_json(node_list)


def add_node(request):
    node = json.loads(request.body)
    status = function.add_node(node)
    return render_json(status)


def del_node(request):
    node_id = json.loads(request.body)
    status = function.del_node(node_id)
    return render_json(status)


def select_node(request):
    node_id = json.loads(request.body)
    node_list = function.select_node(node_id)
    return render_json(node_list)


def truncate_node(request):
    status = function.truncate_node()
    return render_json(status)