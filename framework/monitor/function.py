# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
import json
from models import JobUnit,ChartUnit,Common,BasicUnit,FlowUnit
import tools
import time
from django.forms.models import model_to_dict


def unit_show(request):
    unit = Common.objects.all()
    res_list = []
    for i in unit:
        dic = {
            'id': i.id,
            'unit_name': i.unit_name,
            'unit_type': i.unit_type,
            'editor': i.editor,
            'edit_time': str(i.edit_time),
            'font_size': i.font_size,
            'height': i.height,
            'wide': i.wide,
            'switch': i.switch,
            'start_time': str(i.start_time),
            'end_time': str(i.end_time),
            'cycle': i.cycle,
        }
        res_list.append(dic)
    return res_list


def select_unit(request):
    try:
        res = request.body
        res_list = []
        unit_list = []
        res1 = "{}".format(res)
        if len(res1) == 0:
            res_list = unit_show(request)
        else:
            if res1.isdigit():
                if Common.objects.filter(id=int(res1)).exists():
                    unit = Common.objects.filter(id=int(res1))
            if Common.objects.filter(unit_name=res1).exists():
                unit = Common.objects.filter(unit_name=res1)
            if Common.objects.filter(unit_type=res1).exists():
                unit = Common.objects.filter(unit_type=res1)
            if Common.objects.filter(editor=res1).exists():
                unit = Common.objects.filter(editor=res1)
            for i in unit:
                dic = {
                    'id': i.id,
                    'unit_name': i.unit_name,
                    'unit_type': i.unit_type,
                    'editor': i.editor,
                    'edit_time': str(i.edit_time),
                    'font_size': i.font_size,
                    'height': i.height,
                    'wide': i.wide,
                    'switch': i.switch,
                    'start_time': str(i.start_time),
                    'end_time': str(i.end_time),
                    'cycle': i.cycle,
                }
                res_list.append(dic)
        return res_list

    except Exception as e:
        return None


def delete_unit(request):

    try:
        res = json.loads(request.body)
        unit_id = res['unit_id']
        Common.objects.filter(id=unit_id).delete()
        if BasicUnit.objects.filter(unit_id=unit_id).exists():
            BasicUnit.objects.filter(unit_id=unit_id).delete()
        if ChartUnit.objects.filter(unit_id=unit_id).exists():
            ChartUnit.objects.filter(unit_id=unit_id).delete()
        if JobUnit.objects.filter(unit_id=unit_id).exists():
            JobUnit.objects.filter(unit_id=unit_id).delete()
        if FlowUnit.objects.filter(unit_id=unit_id).exists():
            FlowUnit.objects.filter(unit_id=unit_id).delete()

    except Exception as e:
        res1 = tools.error_result(e)
        return res1


def add_unit(request):

    res = json.loads(request.body)


    unit_type = res['unit_type']
    if res['unit_type'] == 'first':
        unit_type = '基本单元类型'
        add_dic = {
            'contents': res['data']['contents'],
            'sql_file_interface': res['data']['sql_file_interface'],
            'sql': res['data']['sql'],
            'rules': res['data']['rules'],
            'server': res['data']['server'],
            'file': res['data']['file'],
            'urls': res['data']['urls'],
            'param': res['data']['param'],
        }
    if res['unit_type'] == 'second':
        unit_type = '图表单元类型'
        add_dic = {
            'chart_type': res['data']['chart_type'],
            'contents': res['data']['contents'],
            'sql': res['data']['sql'],
            'rules': res['data']['rules'],
        }
    if res['unit_type'] == 'third':
        unit_type = '作业单元类型'
        add_dic = {
            'contents': res['data']['contents'],
            'job_mould': res['data']['job_mould'],
            'NODE_KEY': res['data']['NODE_KEY'],
            'server': res['data']['server'],
        }

    if res['unit_type'] == 'fourth':
        unit_type = '流程单元类型'
        add_dic = {
            'flow_mould': res['data']['flow_mould'],
            'param': res['data']['param1']+res['data']['param2'],
            'node': res['data']['node'],
        }
    common_dic = {
        'unit_name': res['unit_name'],
        'unit_type': unit_type,
        'editor': 'chenyi',
        'font_size': res['data']['font_size'],
        'height': res['data']['height'],
        'wide': res['data']['wide'],
        'cycle': res['data']['cycle'],
        'start_time': "{}:00".format(res['data']['start_time']),
        'end_time': "{}:00".format(res['data']['end_time']),
        'switch': 1,
    }
    Common.objects.create(**common_dic)
    unit_id = Common.objects.get(unit_name=res['unit_name']).id
    add_dic['unit_id'] = unit_id
    if res['unit_type'] == 'first':
        BasicUnit.objects.create(**add_dic)
    if res['unit_type'] == 'second':
        ChartUnit.objects.create(**add_dic)
    if res['unit_type'] == 'third':
        JobUnit.objects.create(**add_dic)
    if res['unit_type'] == 'fourth':
        FlowUnit.objects.create(**add_dic)
    res = unit_show(request)
    return res






# def edit_unit(request):
#
#     try:
#         res =request.body
#         res1 = json.loads(res)
#         unit_id = res1['unit_id']
#         font_size1 = res1['font_size']
#         hight1 = res1['height']
#         wide1 = res1['width']
#         unit_name1=res1['unit_name']
#         unit_administration.objects.filter(id=unit_id).update(font_size=font_size1)
#         unit_administration.objects.filter(id=unit_id).update(hight=hight1)
#         unit_administration.objects.filter(id=unit_id).update(wide=wide1)
#         unit_administration.objects.filter(id=unit_id).update(unit_name=unit_name1)
#         return None
#     except Exception as e:
#
#         res2 = tools.error_result(e)
#         return res2




