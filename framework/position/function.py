# -*- coding: utf-8 -*-
from __future__ import division
import json
import math
import sys
from models import JobInstance, Localuser
from django.forms.models import model_to_dict
from shell_app import tools
from django.db.models import Q
from django.core.paginator import Paginator
from logmanagement.function import add_log,make_log_info,get_active_user
import datetime


def show(request):
    res = json.loads(request.body)
    limit = res['limit']
    page = res['page']
    #查出id大于等于1的岗位（岗位id=1是无岗位人员）
    job = JobInstance.objects.filter(id__gt=1)
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
        x.create_time = str(x.create_time)
        x.edit_time = str(x.edit_time)
        dic = {
            'id': x.id,
            'user_name': tmp,
            'pos_name': x.pos_name,
            'create_time':x.create_time,
            'creator':x.creator,
            'edit_time':x.edit_time,
            'editor':x.editor,
            'page_count': pages
        }
        res_list.append(dic)
    return res_list


def select_job(request):
    res = json.loads(request.body)
    limit = res['limit']
    page = res['page']
    search = res['search'].strip()
    res1 = search
    res_list = []
    tmp = JobInstance.objects.filter(id__gt=1)
    #按岗位查询
    job = tmp.filter(Q(pos_name__contains=res1))
    #按人名查询
    users = Localuser.objects.filter(Q(user_name__contains=res1))
    for i in users:
        user_pos = i.user_pos_id
        temp = JobInstance.objects.filter(id=user_pos)
        job = job | temp
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
        x.create_time = str(x.create_time)
        x.edit_time = str(x.edit_time)
        dic = {
            'id': x.id,
            'user_name': tmp,
            'pos_name': x.pos_name,
            'create_time':x.create_time,
            'creator':x.creator,
            'edit_time':x.edit_time,
            'editor':x.editor,
            'page_count': pages
        }
        res_list.append(dic)
    return res_list


def delete_job(request):
    try:
        res = json.loads(request.body)
        id = res['id']
        res1 = JobInstance.objects.get(id=id).delete()
        info = make_log_info(u'删除岗位', u'业务日志', u'JobInstance', sys._getframe().f_code.co_name, get_active_user(request)['data']['bk_username'], '成功', '无')
    except Exception as e:
        res1 = tools.error_result(e)
        info = make_log_info(u'删除岗位', u'业务日志', u'JobInstance', sys._getframe().f_code.co_name, get_active_user(request)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return res1


def add_job(request):
    try:
        res = json.loads(request.body)
        tmp = get_active_user(request)
        nowPerson = tmp['data']['bk_username']
        res['creator'] = nowPerson
        re = JobInstance.objects.create(**res)
        info = make_log_info(u'增加岗位', u'业务日志', u'JobInstance',sys._getframe().f_code.co_name, get_active_user(request)['data']['bk_username'],'成功','无')
    except Exception, e:
        re = tools.error_result(e)
        info = make_log_info(u'增加岗位', u'业务日志', u'JobInstance',sys._getframe().f_code.co_name, get_active_user(request)['data']['bk_username'], '失败',repr(e))
    add_log(info)
    return re


def add_person(request):
    #外键关联，user_pos不能为空，把岗位id=1 的设为无岗位人员
    try:
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
            Localuser.objects.filter(user_name=k).update(user_pos='1')
        info = make_log_info(u'岗位人员增加或移除', u'业务日志', u'JobInstance', sys._getframe().f_code.co_name, get_active_user(request)['data']['bk_username'],'成功', '无')
    except Exception, e:
        res2 = tools.error_result(e)
        info = make_log_info(u'岗位人员增加或移除', u'业务日志', u'JobInstance', sys._getframe().f_code.co_name, get_active_user(request)['data']['bk_username'],'失败', repr(e))
    add_log(info)
    return res2


def edit_job(request):
    try:
        res = json.loads(request.body)
        id = res['id']
        posname = res['pos_name']
        #获取系统使劲按
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #获取当前用户
        tmp = get_active_user(request)
        nowPerson = tmp['data']['bk_username']
        r1 = JobInstance.objects.filter(id=id).update(pos_name=posname,edit_time=nowTime,editor=nowPerson)
        info = make_log_info(u'编辑岗位', u'业务日志', u'JobInstance',sys._getframe().f_code.co_name, get_active_user(request)['data']['bk_username'],'成功', '无')
    except Exception, e:
        r1 = tools.error_result(e)
        info = make_log_info(u'编辑岗位', u'业务日志', u'JobInstance', sys._getframe().f_code.co_name, get_active_user(request)['data']['bk_username'],'失败', repr(e))
    add_log(info)
    return r1


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
    #蓝鲸所有用户
    filter_list = get_user(request)
    temp = dict_get(filter_list['data'], u'bk_username', None)
    #找出所有无岗位的人员（岗位id=1）
    users = Localuser.objects.all()
    tmp = []
    for j in users:
        for i in range(len(temp)):
            if temp[i] == j.user_name:
                if j.user_pos_id == 1:
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

def get_active_user(request):
    """
    通过蓝鲸获取当前用户
    :param request:
    :return:            dict
    """
    client = tools.interface_param(request)
    res = client.bk_login.get_user({})
    return res

def synchronize(request):
    """
        用户同步
        """
    try:
        res = get_user(request)
        reslist = res['data']
        users = Localuser.objects.all()
        #判断本地用户与蓝鲸用户，以蓝鲸的为准，多了删除，少了增加，变了更新
        for i in reslist:
            flag1 = 0
            for j in users:
                if i['bk_username'] == j.user_name:
                    Localuser.objects.filter(user_name=j.user_name).update(mobile_no=i['phone'],email=i['email']) #,open_id=i['wx_userid']
                    flag1=1
            if flag1 == 0:
                Localuser.objects.create(user_name=i['bk_username'],user_pos_id=1,mobile_no=i['phone'], email=i['email']) #, open_id=i['wx_userid']

        for x in users:
            flag2 = 0
            for y in reslist:
                if x.user_name == y['bk_username']:
                    flag2 = 1
            if flag2 == 0:
                Localuser.objects.filter(user_name=x.user_name).delete()
        info = make_log_info(u'同步蓝鲸用户', u'业务日志', u'Localuser',sys._getframe().f_code.co_name, get_active_user(request)['data']['bk_username'], '成功', '无')
    except Exception, e:
        r1 = tools.error_result(e)
        info = make_log_info(u'同步蓝鲸用户', u'业务日志', u'Localuser',sys._getframe().f_code.co_name, get_active_user(request)['data']['bk_username'],'失败', repr(e))
    add_log(info)
    return  0