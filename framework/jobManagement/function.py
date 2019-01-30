# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
import json
from models import JobInstance,Localuser
from shell_app import tools
import time
from django.forms.models import model_to_dict


def show(request):
    job = JobInstance.objects.all()
    users = Localuser.objects.all()
    res_list = []
    for x in job:
        tmp = []
        for y in users:
            if x.id == y.user_pos:
                tmp.append(y.user_name+' ')
        dic = {
            'id':x.id,
            'user_name': tmp,
            'pos_name': x.pos_name
        }
        res_list.append(dic)
    return res_list

def select_job(request):
    try:
        res = request.body
        res_list = []
        res1 = "{}".format(res)
        if len(res1) == 0:
            res_list = show(request)
        else:
            if res1.isdigit():
                if JobInstance.objects.filter(id=int(res1)).exists():
                    job = JobInstance.objects.filter(id=int(res1))
            if JobInstance.objects.filter(pos_name=res1).exists():
                job = JobInstance.objects.filter(pos_name=res1)
            # if JobInstance.objects.filter(User_name=res1).exists():
            #     job = JobInstance.objects.filter(User_name=res1)
            for x in job:
                tmp = []
                users = Localuser.objects.filter(user_pos=x.id)
                for y in users:
                    if x.id == y.user_pos:
                        tmp.append(y.user_name + ' ')
                dic = {
                    'id': x.id,
                    'user_name': tmp,
                    'pos_name': x.pos_name
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
    res2 = dict_get(res['data2'],u'pinyin',None)
    res3 = res['value2']
    tmp = res2
    for i in res3:
        Localuser.objects.filter(user_name=i).update(user_pos=id)
        for j in res2:
            if i == j:
                tmp.remove(i)
    for k in tmp:
        Localuser.objects.filter(user_name=k).update(user_pos=None)
    return res2


def edit_job(request):
    res = json.loads(request.body)
    id = res['id']
    posname = res['pos_name']
    rl = JobInstance.objects.filter(id=id).update(pos_name =posname )
    return rl

def dict_get(list, objkey, default):
    """
        获得列表的多个字典中对应key的value值
    """
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
        result = client.bk_login.get_all_users({})                  # 获取所有用户信息

    except Exception, e:
        result = tools.error_result(e)
    return result

def filter_user(request):
    """
    筛选用户
    :param request:
    :return:
    """
    filter_list = get_user(request)
    temp = dict_get(filter_list['data'], u'bk_username', None)
    users = Localuser.objects.all()
    tmp = []
    for j in users:
        for i in range(len(temp)):
                if temp[i] == j.user_name:
                    if j.user_pos == None:
                        tmp.append(temp[i])
    return tmp




