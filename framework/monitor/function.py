# -*- coding: utf-8 -*-
from __future__ import division
import json
import math
from models import *
from monitorScene.models import Scene
import tools


def unit_show(request):

    res = json.loads(request.body)
    limit = res['limit']
    page = res['page']
    start_page = limit*page-9
    unit = Monitor.objects.all()[start_page-1:start_page+9]
    unit2 = Monitor.objects.all().values('id')
    page_count = math.ceil(len(unit2)/10)
    print(page_count)
    res_list = []
    for i in unit:
        dic = {
            'id': i.id,
            'monitor_name': i.monitor_name,
            'monitor_type': i.monitor_type,
            'editor': i.editor,
            'font_size': i.font_size,
            'height': i.height,
            'width': i.width,
            'status': i.status,
            'edit_time': str(i.edit_time),
            'start_time': str(i.start_time),
            'end_time': str(i.end_time),
            'period': i.period,
            'page_count': page_count,
        }
        res_list.append(dic)
    display_list = []
    param = {

    }
    return res_list


def select_unit(request):
    pass
    try:
        res = request.body
        res_list = []
        res1 = "{}".format(res)
        if len(res1) == 0:
            res_list = unit_show(request)
        else:
            if res1.isdigit():
                if Monitor.objects.filter(id=int(res1)).exists():
                    unit = Monitor.objects.filter(id=int(res1))
            if Monitor.objects.filter(unit_name=res1).exists():
                unit = Monitor.objects.filter(unit_name=res1)
            if Monitor.objects.filter(unit_type=res1).exists():
                unit = Monitor.objects.filter(unit_type=res1)
            if Monitor.objects.filter(editor=res1).exists():
                unit = Monitor.objects.filter(editor=res1)
            for i in unit:
                dic = {
                    'id': i.id,
                    'monitor_name': i.monitor_name,
                    'monitor_type': i.monitor_type,
                    'editor': i.editor,
                    'edit_time': str(i.edit_time),
                    'font_size': i.font_size,
                    'height': i.height,
                    'width': i.width,
                    'status': i.status,
                    'start_time': str(i.start_time),
                    'end_time': str(i.end_time),
                    'period': i.period,
                }
                res_list.append(dic)
        return res_list

    except Exception as e:
        return None


def delete_unit(request):
    pass

    try:
        res = json.loads(request.body)
        unit_id = res['unit_id']
        Monitor.objects.filter(id=unit_id).delete()
        if Scene.objects.filter(item_id=unit_id).exists():
            Scene.objects.filter(item_id=unit_id).delete()

    except Exception as e:
        res1 = tools.error_result(e)
        return res1


def add_unit(request):

    res = json.loads(request.body)
    monitor_type = res['monitor_type']
    print(monitor_type)
    if res['monitor_type'] == 'first':
        monitor_type = '基本单元类型'
    if res['monitor_type'] == 'second':
        monitor_type = '图表单元类型'
    if res['monitor_type'] == 'third':
        monitor_type = '作业单元类型'
    if res['monitor_type'] == 'fourth':
        monitor_type = '流程元类型'
    add_dic = res['data']
    add_dic['monitor_name'] = res['monitor_name']
    add_dic['monitor_type'] = monitor_type
    add_dic['jion_id'] = 3
    add_dic['status'] = 0
    add_dic['creator'] = 'admin'
    add_dic['editor'] = 'admin'
    Monitor.objects.create(**add_dic)
    return None


def edit_unit(request):
    res = json.loads (request.body)
    monitor_type = res['monitor_type']
    print(monitor_type)
    if res['monitor_type'] == 'first':
        monitor_type = '基本单元类型'
    if res['monitor_type'] == 'second':
        monitor_type = '图表单元类型'
    if res['monitor_type'] == 'third':
        monitor_type = '作业单元类型'
    if res['monitor_type'] == 'fourth':
        monitor_type = '流程元类型'
    add_dic = res['data']
    add_dic['monitor_name'] = res['monitor_name']
    add_dic['monitor_type'] = monitor_type
    add_dic['jion_id'] = 3
    add_dic['status'] = 0
    add_dic['creator'] = 'admin'
    add_dic['editor'] = 'admin'
    Monitor.objects.filter(monitor_name=res['monitor_name']).update(**add_dic)
    return None
