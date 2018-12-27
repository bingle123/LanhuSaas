# -*- coding: utf-8 -*-
from models import unit_administration
import tools


def unit_show(request):

    limit = 10
    tools.page_paging(request, limit)
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


def edit_unit(request):
    pass


