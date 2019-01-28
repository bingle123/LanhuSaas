# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
import json
from models import Scene
from models import position_scene
# from models import scene_monitor
from jobManagement.models import JobInstance

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
       "position_id":senceModel["pos"]
   }
   position_scene.objects.create(**senceModel3)
   return None

def select_table(request):
    res = request.body
    res_list = []
    if(len(res) == 0):
         res_list=monitor_show(request)
         return res_list
    else:
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
    senceModel3 = {
        "scene_id": model['data']['id'],
        "position_id": model["pos"]
    }
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
