# -*- coding: utf-8 -*-
from __future__ import division
import json
import math
from django.core.paginator import Paginator
from django.forms import model_to_dict
from models import Scene
from models import position_scene
from monitor.models import scene_monitor,Monitor
from monitor import tools
from position.models import JobInstance


def monitor_show(request):
    monitor = Scene.objects.all()
    res_list = []
    for i in monitor:
        dic = {
            'id': i.id,
            'scene_name': i.scene_name,
            'scene_startTime': str(i.scene_startTime),
            'scene_endTime': str(i.scene_endTime),
            'scene_creator': i.scene_creator,
            'scene_creator_time': str(i.scene_creator_time),
            'scene_editor': i.scene_editor,
            'scene_editor_time': str(i.scene_editor_time),
            'pos_name':''
        }
        position = position_scene.objects.filter(scene=i.id)
        for c in position:
            job = JobInstance.objects.filter(id=c.position_id)
            for j in job:
                jobs = {
                    "pos_name" : j.pos_name
                }
                dic['pos_name']=jobs["pos_name"]
        res_list.append(dic)
    return res_list


def addSence(request):
   res = request.body
   senceModel = json.loads(res)
   senceModel2 = {
       "scene_name":senceModel['data']['scene_name'],
       "scene_startTime":senceModel['data']["scene_startTime"],
       "scene_endTime":senceModel['data']["scene_endTime"],
       "scene_creator":"admin"
   }
   Scene.objects.create(**senceModel2)
   id = Scene.objects.last()
   senceModel3 = {
       "scene":id,
       "position_id":senceModel['data']["pos_name"]
   }
   position_scene.objects.create(**senceModel3)
   return None


def select_table(request):
    res = request.body
    res_list = []
    monitor =Scene.objects.filter(scene_name__contains=res)
    for i in monitor:
        dic = {
            'id': i.id,
            'scene_name': i.scene_name,
            'scene_startTime': str(i.scene_startTime),
            'scene_endTime': str(i.scene_endTime),
            'scene_creator': i.scene_creator,
            'scene_creator_time': str(i.scene_creator_time),
            'scene_editor': i.scene_editor,
            'scene_editor_time': str(i.scene_editor_time),
        }
        position = position_scene.objects.filter(scene=i.id)
        for c in position:
            job = JobInstance.objects.filter(id=c.position_id)
            for j in job:
                jobs = {
                    "pos_name": j.pos_name
                }
                dic['pos_name'] = jobs["pos_name"]
        res_list.append(dic)
        print res_list
    return res_list


def delect(request):
    Scene.objects.filter(id=request.body).delete()
    position_scene.objects.filter(scene=request.body).delete()
    return ""


def editSence(request):
    model = json.loads(request.body)
    senceModel2 = {
        "scene_name": model['data']['scene_name'],
        "scene_startTime": model['data']["scene_startTime"],
        "scene_endTime": model['data']["scene_endTime"],
        "scene_editor":"admin"
    }
    Scene.objects.filter(id=model['data']['id']).update(**senceModel2)
    scene = Scene.objects.get(id=model['data']['id'])
    scene.save()
    job =JobInstance.objects.filter(pos_name=model['data']["pos_name"])
    for j in job:
        senceModel3 = {
        "scene_id": model['data']['id'],
        "position_id": j.id
        }
        print senceModel3
    position_scene.objects.filter(scene=senceModel3['scene_id']).update(**senceModel3)
    return None


def pos_name(request):
    job=JobInstance.objects.all()
    res_list = []
    for i in job:
        dic = {
            'id': i.id,
            'pos_name': i.pos_name
        }
        res_list.append(dic)
    return res_list


def paging(request):
    res = json.loads(request.body)
    page = res['page']
    limit = res['limit']
    start_page = limit*page-9
    monitor = Scene.objects.all()[start_page-1:start_page+9]
    monitor2 = Scene.objects.all().values('id')
    page_count = math.ceil(len(monitor2)/10)
    res_list = []
    for i in monitor:
        dic = {
            'id': i.id,
            'scene_name': i.scene_name,
            'scene_startTime': str(i.scene_startTime),
            'scene_endTime': str(i.scene_endTime),
            'scene_creator': i.scene_creator,
            'scene_creator_time': str(i.scene_creator_time),
            'scene_editor': i.scene_editor,
            'scene_editor_time': str(i.scene_editor_time),
            'pos_name': '',
            'page_count': page_count,
        }
        position = position_scene.objects.filter(scene=i.id)
        for c in position:
            job = JobInstance.objects.filter(id=c.position_id)
            for j in job:
                jobs = {
                    "pos_name": j.pos_name
                }
                dic['pos_name'] = jobs["pos_name"]
        res_list.append(dic)
    return res_list


def scene_show(res):

    type = res['type']
    limit = res['limit']
    page = res['page']
    if type == 0:
        base_unit = Monitor.objects.filter(monitor_type='基本单元类型')
        base_page_data, base_page_count = tools.page_paging(base_unit,limit,page)
        chart_unit = Monitor.objects.filter (monitor_type='图表单元类型')
        chart_page_data, chart_page_count = tools.page_paging (chart_unit, limit, page)
        job_unit = Monitor.objects.filter (monitor_type='作业单元类型')
        job_page_data, job_page_count = tools.page_paging (job_unit, limit, page)
        flow_unit = Monitor.objects.filter (monitor_type='流程单元类型')
        flow_page_data, flow_page_count = tools.page_paging (flow_unit, limit, page)
        base_list = tools.obt_dic (base_page_data, base_page_count)
        chart_list = tools.obt_dic (chart_page_data, chart_page_count)
        job_list = tools.obt_dic (job_page_data, job_page_count)
        flow_list = tools.obt_dic (flow_page_data, flow_page_count)
        res_dic = {
            'base_list': base_list,
            'chart_list': chart_list,
            'job_list': job_list,
            'flow_list': flow_list,
        }
    elif type == 1:
        base_unit = Monitor.objects.filter (monitor_type='基本单元类型')
        base_page_data, base_page_count = tools.page_paging (base_unit, limit, page)
        base_list = tools.obt_dic (base_page_data, base_page_count)
        res_dic = {
            'base_list': base_list,
        }
    elif type == 2:
        chart_unit = Monitor.objects.filter (monitor_type='图表单元类型')
        chart_page_data, chart_page_count = tools.page_paging (chart_unit, limit, page)
        chart_list = tools.obt_dic (chart_page_data, chart_page_count)
        res_dic = {
            'chart_list': chart_list,
        }
    elif type == 3:
        job_unit = Monitor.objects.filter (monitor_type='作业单元类型')
        job_page_data, job_page_count = tools.page_paging (job_unit, limit, page)
        job_list = tools.obt_dic (job_page_data, job_page_count)
        res_dic = {
            'job_list': job_list,
        }
    elif type == 4:
        flow_unit = Monitor.objects.filter (monitor_type='流程单元类型')
        flow_page_data, flow_page_count = tools.page_paging (flow_unit, limit, page)
        flow_list = tools.obt_dic (flow_page_data, flow_page_count)
        res_dic = {
            'flow_list': flow_list,
        }
    result = tools.success_result(res_dic)
    return result