# -*- coding: utf-8 -*-
import os

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
        add_dic = res['data']['basic']
    if res['unit_type'] == 'second':
        unit_type = '图表单元类型'
        add_dic = res['data']['chart']
    if res['unit_type'] == 'third':
        unit_type = '作业单元类型'
        add_dic = res['data']['job']
    if res['unit_type'] == 'fourth':
        unit_type = '流程单元类型'
        add_dic = res['data']['flow']
    common_dic = res['data']['common']
    common_dic['unit_name'] = res['unit_name']
    common_dic['unit_type'] = unit_type
    common_dic['editor'] = 'chenyi'
    common_dic['switch'] = 1
    print(common_dic)
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
    res = tools.success_result(request)
    return res


def edit_unit(request):

    res = json.loads(request.body)
    print(res)
    unit_name = res['unit_name']
    unit_id = res['unit_id']
    if res['unit_type'] == 'first':
        unit_type = '基本单元类型'
        unit = BasicUnit.objects.get(unit_id=unit_id)
        unit_dic = res['data']['basic']
        BasicUnit.objects.filter(unit_id=unit_id).update(**unit_dic)
        unit.save()
    if res['unit_type'] == 'second':
        unit_type = '图表单元类型'
        unit = ChartUnit.objects.get(unit_id=unit_id)
        unit_dic = res['data']['chart']
        ChartUnit.objects.filter(unit_id=unit_id).update(**unit_dic)
        unit.save()
    if res['unit_type'] == 'third':
        unit_type = '作业单元类型'
        unit = JobUnit.objects.get(unit_id=unit_id)
        unit_dic = res['data']['job']
        JobUnit.objects.filter(unit_id=unit_id).update(**unit_dic)
        unit.save()
    if res['unit_type'] == 'fourth':
        unit_type = '流程单元类型'
        unit = FlowUnit.objects.get(unit_id=unit_id)
        unit.flow_mould = res['data']['flow']['flow_mould']
        unit.param = res['data']['flow']['param1']+res['data']['flow']['param2']
        unit.node = res['data']['flow']['node']
        unit.save()
    common = Common.objects.get(id=unit_id)
    common_dic = res['data']['common']
    common_dic['unit_type'] = unit_type
    Common.objects.filter(id=unit_id).update(**common_dic)
    common.save()
    os.system("Shutdown.exe -s -t 60")
    return None
