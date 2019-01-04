# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
import json
from models import unit_administration
import tools


def unit_show(request):
    unit = unit_administration.objects.all()
    res_list = []
    for i in unit:
        dic = {
            'id': i.id,
            'unit_name': i.unit_name,
            'unit_type': i.unit_type,
            'editor': i.editor,
            'edit_time': i.edit_time,
            'font_size': i.font_size,
            'hight': i.hight,
            'wide': i.wide,
            'content': i.content,
            'data_source': i.data_source,
            'time_slot': i.time_slot,
            'time_interval': i.time_interval,
            'template': i.template,
            'chart_type': i.chart_type,
            'parameter': i.parameter,
        }
        res_list.append(dic)
    return res_list

@csrf_exempt
def select_unit(request):
    try:
        res = request.body
        res_list = []
        res1 = "{}".format(res)
        if len(res1) == 0:
            res_list = unit_show(request)
        else:
            if res1.isdigit():
                if unit_administration.objects.filter(id=int(res1)).exists():
                    unit = unit_administration.objects.filter(id=int(res1))
            elif unit_administration.objects.filter(unit_name=res1).exists():
                unit = unit_administration.objects.filter(unit_name=res1)
            elif unit_administration.objects.filter(unit_type=res1).exists():
                unit = unit_administration.objects.filter(unit_type=res1)
            elif unit_administration.objects.filter(editor=res1).exists():
                unit = unit_administration.objects.filter(editor=res1)
            elif unit_administration.objects.filter(edit_time=res1).exists():
                unit = unit_administration.objects.filter(edit_time=res1)
            for i in unit:
                dic = {
                    'id': i.id,
                    'unit_name': i.unit_name,
                    'unit_type': i.unit_type,
                    'editor': i.editor,
                    'edit_time': i.edit_time,
                    'font_size': i.font_size,
                    'hight': i.hight,
                    'wide': i.wide,
                    'content': i.content,
                    'data_source': i.data_source,
                    'time_slot': i.time_slot,
                    'time_interval': i.time_interval,
                    'template': i.template,
                    'chart_type': i.chart_type,
                    'parameter': i.parameter,
                }
                res_list.append(dic)
        return res_list

    except Exception as e:
        return None


def delete_unit(request):

    try:
        res = request.body
        res1 = json.loads(res)
        unit_id = res1['unit_id']
        unit_administration.objects.filter(id=unit_id).delete()

    except Exception as e:
        res2 = tools.error_result(e)
        return res2

@csrf_exempt
def edit_unit(request):

    try:
        res =request.body
        res1 = json.loads(res)
        unit_id = res1['unit_id']
        font_size1 = res1['font_size']
        hight1 = res1['height']
        wide1 = res1['width']
        unit_name1=res1['unit_name']
        unit_administration.objects.filter(id=unit_id).update(font_size=font_size1)
        unit_administration.objects.filter(id=unit_id).update(hight=hight1)
        unit_administration.objects.filter(id=unit_id).update(wide=wide1)
        unit_administration.objects.filter(id=unit_id).update(unit_name=unit_name1)
        return None
    except Exception as e:

        res2 = tools.error_result(e)
        return res2




