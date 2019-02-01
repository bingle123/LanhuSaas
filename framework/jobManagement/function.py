# -*- coding: utf-8 -*-
from __future__ import division
import json
import math
from models import JobInstance, Localuser
from django.forms.models import model_to_dict
from shell_app import tools
from django.db.models import Q
from django.core.paginator import Paginator


def show(request):
    res = json.loads(request.body)
    limit = res['limit']
    page = res['page']
    job = JobInstance.objects.all()
    users = Localuser.objects.all()
    p = Paginator(job, limit)
    count = p.page_range
    pages = count[-1]
    res_list = []
    current_page = p.page(page)
    for x in current_page.object_list:
        tmp = []
        for y in users:
            if x.id == y.user_pos.id:
                tmp.append(y.user_name + ' ')
        dic = {
            'id': x.id,
            'user_name': tmp,
            'pos_name': x.pos_name,
            'page_count': pages
        }
        res_list.append(dic)
    return res_list


def select_job(request):
    res = json.loads(request.body)
    limit = res['limit']
    page = res['page']
    search = res['search']
    res1 = search
    res_list = []
    job = JobInstance.objects.filter(Q(pos_name__contains=res1) | Q(creator__icontains=res1))
    users = Localuser.objects.all()
    p = Paginator(job, limit)
    count = p.page_range
    pages = count[-1]
    current_page = p.page(page)
    for x in current_page.object_list:
        tmp = []
        for y in users:
            if x.id == y.user_pos.id:
                tmp.append(y.user_name + ' ')
        dic = {
            'id': x.id,
            'user_name': tmp,
            'pos_name': x.pos_name,
            'page_count': pages
        }
        res_list.append(dic)
    return res_list


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
    res2 = dict_get(res['data2'], u'pinyin', None)
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
    rl = JobInstance.objects.filter(id=id).update(pos_name=posname)
    return rl


def dict_get(list, objkey, default):
    """
        获得列表的多个字典中对应key的value值
    """
    tmp = list
    tmp2 = []
    for i in tmp:
        if type(i) is dict:
            for k, v in i.items():
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


def get_tree(request):
    job = JobInstance.objects.all()
    users = Localuser.objects.all()
    res_list = []
    for x in job:
        tmp = []
        for y in users:
            if x.id == y.user_pos_id:
                dic1 = {
                    'label' : y.user_name
                }
                tmp.append(dic1)
        dic = {
            'id': x.id,
            'children': tmp,
            'label': x.pos_name,
        }
        res_list.append(dic)
    return res_list