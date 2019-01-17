# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
import json
from models import JobUnit,ChartUnit,Common,BasicUnit,FlowUnit
import tools
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

@csrf_exempt
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
                    unit_list.append(unit)
            if Common.objects.filter(unit_name=res1).exists():
                unit = Common.objects.filter(unit_name=res1)
                unit_list.append (unit)
            if Common.objects.filter(unit_type=res1).exists():
                unit = Common.objects.filter(unit_type=res1)
                unit_list.append (unit)
            if Common.objects.filter(editor=res1).exists():
                unit = Common.objects.filter(editor=res1)
                unit_list.append (unit)
            if Common.objects.filter(edit_time=res1).exists():
                unit = Common.objects.filter(edit_time=res1)
                unit_list.append(unit)
            for i in unit_list:
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


# def delete_unit(request):
#
#     try:
#         res = request.body
#         res1 = json.loads(res)
#         unit_id = res1['unit_id']
#         unit_administration.objects.filter(id=unit_id).delete()
#
#     except Exception as e:
#         res2 = tools.error_result(e)
#         return res2
#
# @csrf_exempt
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




