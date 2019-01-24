# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
import json
from models import JobInstance
from shell_app import tools
import time
from django.forms.models import model_to_dict


def job_show(request):
    job = JobInstance.objects.all()
    res_list = []
    for i in job:
        dic = {
            'id': i.id,
            'job_name': i.job_name,
            'create_time': str(i.create_time),
            'create_person': i.create_person,
            'edit_time': str(i.edit_time),
            'edit_person':i.edit_person,
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
    jobname = res['jobname']
    username = res['username']
    if not username.strip():
        username = res['data'][1]['pinyin']
        re = JobInstance.objects.filter(id=id).update(User_name=username)
        return re
    else:
        re2 = dict_get(res['data'],u'pinyin',None)
        for i in re2:
            JobInstance.objects.create(Job_name=jobname,User_name=i)
        return re2

def edit_job(request):
    res = json.loads(request.body)
    id = res['id']
    Job_name = res['Job_name']
    rl = JobInstance.objects.filter(id=id).update(Job_name =Job_name )
    return rl

def dict_get(list, objkey, default):                    #获得列表的多个字典中对应key的value值
    tmp = list
    tmp2 = []
    for i in tmp:
        if type(i) is dict:
            for k,v in i.items():
                if k == objkey:
                    tmp2.append(v)
    if len(tmp2):
        return tmp2
    else:
        return default

def get_user(request):
    """
    获取所有用户
    :param request:
    :return:
    """
    try:
        client = tools.interface_param(request)
        result = client.bk_login.get_all_users({})  # 获取所有用户信息
        temp = dict_get(result['data'],u'bk_username',None)
    except Exception, e:
        result = tools.error_result(e)
    return result


