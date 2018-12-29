# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt

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
    res = request.POST.get('send_data')
    res_list = []
    res1 = "{}".format(res)
    print(len(res1))
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
        else:
            unit_administration.objects.filter(edit_time=res1).exists()
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


def delete_unit(request):

    unit_administration.objects.filter(id=1).delete()


def edit_unit(request):

    id = request.POST.get('id')
    unit_name = request.POST.get('unit_name')
    font_size = request.POST.get('font_size')
    hight = request.POST.get('hight')
    wide = request.POST.get('wide')
    chart_type = request.POST.get('chart_type')
    edit_time = request.POST.get('edit_time')
