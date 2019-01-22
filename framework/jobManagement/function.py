# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
import json
from models import JobInstance
import tools
import time
from django.forms.models import model_to_dict


def job_show(request):
    job = JobInstance.objects.all()
    res_list = []
    for i in job:
        dic = {
            'id': i.id,
            'Job_name': i.Job_name,
            'User_name': i.User_name,
            'Start_Time': str(i.Start_Time),
            'Status': i.Status,
            'log':i.log,
        }
        res_list.append(dic)
    return res_list


def select_job(request):
    try:
        res = request.body
        res_list = []
        res1 = "{}".format(res)
        if len(res1) == 0:
            res_list = job_show(request)
        else:
            if res1.isdigit():
                if JobInstance.objects.filter(id=int(res1)).exists():
                    job = JobInstance.objects.filter(id=int(res1))
            if JobInstance.objects.filter(Job_name=res1).exists():
                job = JobInstance.objects.filter(Job_name=res1)
            if JobInstance.objects.filter(User_name=res1).exists():
                job = JobInstance.objects.filter(User_name=res1)
            for i in job:
                dic = {
                    'id': i.id,
                    'Job_name': i.Job_name,
                    'User_name': i.User_name,
                    'Start_Time': str(i.Start_Time),
                    'Status': i.Status,
                    'log':i.log,
                }
                res_list.append(dic)
        return res_list
    except Exception as e:
        return None


def delete_job(request):
    try:
        res = json.loads(request.body)
        id = res['id']
        JobInstance.objects.filter(id=id).delete()
    except Exception as e:
        res1 = tools.error_result(e)
        return res1


def add_job(request):
    res = json.loads(request.body)
    re = JobInstance.objects.create(**res)
    return re

def add_person(request):
    res = json.loads(request.body)
    id = res['id']
    # re = JobInstance.objects.filter(id=id).update(Job_name=)
    # return re

def edit_job(request):
    res1 = json.loads(request.body)
    id = res1['id']
    rl = JobInstance.objects.filter(id=id).update(**res1)
    return rl




