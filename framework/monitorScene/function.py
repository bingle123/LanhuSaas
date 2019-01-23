# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
from models import Scene
import tools

@csrf_exempt
def monitor_show(request):
    monitor = Scene.objects.all()
    res_list = []
    for i in monitor:
        dic = {
            'id': i.id,
            'scene_name': i.scene_name,
            'scene_startTime': str(i.scene_startTime),
            'scene_endTime': str(i.scene_endTime),
            'scene_positions': i.scene_positions,
            'scene_creator': i.scene_creator,
            'scene_creator_time': str(i.scene_creator_time),
            'scene_editor': i.scene_editor,
            'scene_editor_time': str(i.scene_editor_time),
        }


        res_list.append(dic)
    return res_list

def addSence(request):
   res = request.body
   senceModel = json.loads(res)
   print senceModel
   scene_name = senceModel['scene_name']
   scene_positions = senceModel['scene_positions']
   senceModel['scene_creator'] = "admin"
    # Scene.objects.create(**senceModel)
   return res;

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
            'scene_positions': i.scene_positions,
            'scene_creator': i.scene_creator,
            'scene_creator_time': str(i.scene_creator_time),
            'scene_editor': i.scene_editor,
            'scene_editor_time': str(i.scene_editor_time),
        }
        res_list.append(dic)
    return res_list


def delect(request):
    Scene.objects.filter(id=request.body).delete()
    return ""

def editSence(request):
    model = json.loads(request.body)
    Scene.objects.filter(id=model['id']).update(**model)
    scene = Scene.objects.get(id=model['id'])
    scene.save()