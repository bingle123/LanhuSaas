# -*- coding: utf-8 -*-
from __future__ import division
import json
import sys
from models import pos_info, user_info, user_group
from shell_app import tools
from django.db.models import Q
from django.core.paginator import Paginator
from logmanagement.function import add_log, make_log_info
import datetime


def get_noposition_id():
    """
    获取无岗位在岗位表的id
    :return:
    """
    noposition_id = pos_info.objects.get(pos_name=u'管理员').id
    return noposition_id


# 保存两张表修改的信息
def add_group(request):
    res = json.loads(request.body)
    # 不在当前组别下的用户名称
    in_users = res['value4']
    user_list = user_info.objects.all()
    in_users_id = ""
    for user_item in in_users:
        flag = 0
        for user in user_list:
            if int(user_item) == flag:
                in_users_id = in_users_id + str(user.id) + ","
            flag = flag+1
    # 得到在当前组别下的所有用户id
    # 组别名称
    user_group_name =  res['user_group']
    # 当前组别对象
    user_group_list = user_group.objects.get(name=user_group_name)
    user_group_list.user_id_group = in_users_id[:-1]

    user_group_list.save()


    return get_user_group(request)


# 获取用户名称和人员组别
def get_user_group(request):
    user_list = user_info.objects.all()
    user_group_list = user_group.objects.all()
    # 需要获取所有的用户名称 ，还有人员类别表中每个类别上所有用户的id
    users = []
    for user in user_list:
        users.append(user.user_name)

    for group in user_group_list:
        # 切分每组组别中的用户id
        group_id = group.user_id_group.split(",")
        user_ids_item = []
        for group_id_item in group_id:
            flag = 0
            for user in user_list:
                if int(group_id_item) == user.id:
                    user_ids_item.append(str(flag))
                    break
                flag = flag + 1

        group.user_id_group = user_ids_item
    res_list = []
    for pro in user_group_list:
        dic = {
            # 目前所有用户
            'user_name': users,
            # 目前所有组别信息（组别id,组别名称，组别下的人员在用户名称中所在序号）
            'group_list_id': pro.id,
            'group_list_name': pro.name,
            'group_list_user': pro.user_id_group,
        }
        res_list.append(dic)
    return res_list


def show(request):
    """
    显示岗位--人员信息
    :param request:
    :return:
    """
    res = json.loads(request.body)
    # 每页行数
    limit = res['limit']
    # 页数
    page = res['page']
    # 获取无岗位id
    noposition_id = get_noposition_id()
    # 查出id大于等于1的岗位（岗位id=1是无岗位人员）
    position_list = pos_info.objects.filter(~Q(id=noposition_id)).order_by('-create_time')
    user_list = user_info.objects.all()
    # 分页
    p = Paginator(position_list, limit)
    count = p.page_range
    pages = count[-1]
    res_list = []
    current_page = p.page(page)
    for pos in current_page.object_list:
        users = []
        for user in user_list:
            # 岗位对应的人员名
            if pos.id == user.user_pos.id:
                users.append(user.user_name + ' ')
        pos.create_time = str(pos.create_time)
        pos.edit_time = str(pos.edit_time)
        dic = {
            'id': pos.id,
            'user_name': users,
            'pos_name': pos.pos_name,
            'create_time': pos.create_time,
            'creator': pos.creator,
            'edit_time': pos.edit_time,
            'editor': pos.editor,
            'page_count': pages
        }
        res_list.append(dic)
    return res_list


def select_pos(request):
    """
    查询岗位
    :param request:
    :return:
    """
    # 接受前台数据
    res = json.loads(request.body)
    limit = res['limit']
    page = res['page']
    search = res['search'].strip()
    res1 = search
    res_list = []
    # 获取无岗位id
    noposition_id = get_noposition_id()
    # 获取
    position_list = pos_info.objects.filter(~Q(id=noposition_id)).order_by('-create_time')
    # 按岗位查询
    positions = position_list.filter(Q(pos_name__contains=res1))
    # 按人名查询
    users = user_info.objects.filter(Q(user_name__contains=res1))
    # 查询结果整合
    for i in users:
        user_pos = i.user_pos_id
        position = pos_info.objects.filter(id=user_pos)
        positions = positions | position
    user_list = user_info.objects.all()
    # 分页
    p = Paginator(positions, limit)
    count = p.page_range
    pages = count[-1]
    current_page = p.page(page)
    # 根据岗位id匹配用户表的user_pos_id整合返回
    for pos in current_page.object_list:
        usernames = []
        for user in user_list:
            # 匹配
            #
            if pos.id == user.user_pos.id:
                usernames.append(user.user_name + ' ')
        pos.create_time = str(pos.create_time)
        pos.edit_time = str(pos.edit_time)
        dic = {
            'id': pos.id,
            'user_name': usernames,
            'pos_name': pos.pos_name,
            'create_time': pos.create_time,
            'creator': pos.creator,
            'edit_time': pos.edit_time,
            'editor': pos.editor,
            'page_count': pages
        }
        res_list.append(dic)
    return res_list


def delete_pos(request):
    """
    删除岗位
    :param request:
    :return:
    """
    try:
        res = json.loads(request.body)
        id = res['id']
        res1 = pos_info.objects.get(id=id).delete()
        info = make_log_info(u'删除岗位', u'业务日志', u'pos_info', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
    except Exception as e:
        res1 = tools.error_result(e)
        info = make_log_info(u'删除岗位', u'业务日志', u'pos_info', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
    add_log(info)
    return res1


def add_pos(request):
    """
    增加岗位
    :param request:
    :return:
    """
    try:
        re = ''
        res = json.loads(request.body)
        # 获取当前用户
        nowPerson = request.user.username
        res['creator'] = nowPerson
        pos_info.objects.create(**res)
        info = make_log_info(u'增加岗位', u'业务日志', u'pos_info', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
    except Exception, e:
        re = tools.error_result(e)
        info = make_log_info(u'增加岗位', u'业务日志', u'pos_info', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
    add_log(info)
    return re


def add_person(request):
    """
    添加岗位人员
    :param request:
    :return:
    """
    # 外键关联，user_pos不能为空，把岗位id=1 的设为无岗位人员
    try:
        res = json.loads(request.body)
        id = res['id']
        # 穿梭框左边的值
        person_no_positions = dict_get(res['data2'], u'pinyin', None)
        # 穿梭框右边的值
        person_positions = res['value2']
        # 获取无岗位id
        noposition_id = get_noposition_id()
        # 一个用来循环，一个用来存数据
        person_no_positions2 = person_no_positions
        # 增加岗位人员
        for pos_username in person_positions:
            user_info.objects.filter(user_name=pos_username).update(user_pos=id)
            # 把已经赋予岗位的人员从左边移出
            for no_pos_username in person_no_positions:
                if pos_username == no_pos_username:
                    person_no_positions2.remove(pos_username)
        # 移出岗位人员
        for no_pos_username2 in person_no_positions2:
            user_info.objects.filter(user_name=no_pos_username2).update(user_pos=noposition_id)
        info = make_log_info(u'岗位人员增加或移除', u'业务日志', u'pos_info', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
    except Exception, e:
        res = tools.error_result(e)
        info = make_log_info(u'岗位人员增加或移除', u'业务日志', u'pos_info', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
    add_log(info)
    return res


def edit_pos(request):
    """
    编辑岗位
    :param request:
    :return:
    """
    try:
        res = json.loads(request.body)
        id = res['id']
        posname = res['pos_name']
        # 获取系统时间
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 获取当前用户
        nowPerson = request.user.username
        r1 = pos_info.objects.filter(id=id).update(pos_name=posname, edit_time=nowTime, editor=nowPerson)
        info = make_log_info(u'编辑岗位', u'业务日志', u'pos_info', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
    except Exception, e:
        r1 = tools.error_result(e)
        info = make_log_info(u'编辑岗位', u'业务日志', u'pos_info', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
    add_log(info)
    return r1


def dict_get(list, objkey, default):
    """
    获得列表的多个字典中对应key的value值
    :param list:
    :param objkey:
    :param default:
    :return:
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
    获取蓝鲸平台所有用户
    :param request:
    :return:
    """
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
    # 蓝鲸所有用户
    filter_list = get_user(request)
    all_user_names = dict_get(filter_list['data'], u'bk_username', None)
    # 找出所有无岗位的人员
    users = user_info.objects.all()
    users_no_position = []
    # 获取无岗位id
    noposition_id = get_noposition_id()
    for user in users:
        for i in range(len(all_user_names)):
            if all_user_names[i] == user.user_name and user.user_pos_id == noposition_id:
                users_no_position.append(all_user_names[i])
    return users_no_position


def get_tree(request):
    """

    :param request:
    :return:
    """
    # 获得所有的用户信息和岗位信息
    positions = pos_info.objects.all()
    users = user_info.objects.all()

    res_list = []
    for pos in positions:
        children = []
        for user in users:
            if pos.id == user.user_pos_id:
                dic1 = {
                    'label': user.user_name
                }
                children.append(dic1)
        dic = {
            'id': pos.id,
            'children': children,
            'label': pos.pos_name,
        }
        res_list.append(dic)
    return res_list


def synchronize(request):
    """
    用户同步
    :param request:
    :return:
    """
    try:
        res = get_user(request)
        reslist = res['data']
        # 获取无岗位id
        # noposition_id = get_noposition_id()
        # 所有用户
        users = user_info.objects.all()
        # 判断本地用户与蓝鲸用户，以蓝鲸的为准，多了删除，少了增加，变了更新
        # 先蓝鲸用户匹配本地用户,少了增加，变了更新
        for data in reslist:
            flag1 = 0
            for user in users:
                if data['bk_username'] == user.user_name:
                    user_info.objects.filter(user_name=user.user_name).update(mobile_no=data['phone'], email=data['email'],user_type_id=data['bk_role'])
                    flag1 = 1
                    break
            if flag1 == 0:
                if data['bk_role'] == 1:
                    user_pos = 1
                else:
                    user_pos = 2
                user_info.objects.create(user_name=data['bk_username'], user_type_id=data['bk_role'],
                                         mobile_no=data['phone'], email=data['email'],
                                         user_pos_id=user_pos)
        # 后本地用户匹配蓝鲸用户,多了删除
        #for user in users:
            #flag2 = 0
            #for data in reslist:
                # 相同表示存在，就不管
            #   if user.user_name == data['bk_username']:
            #        flag2 = 1
            #   break
            # 表示此用户表中的用户，已经在蓝鲸上删除，在用户表中也删除
            #if flag2 == 0:
                # user_info.objects.filter(user_name=user.user_name).delete()
        info = make_log_info(u'同步蓝鲸用户', u'业务日志', u'user_info', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
        mess = "同步成功"
    except Exception, e:
        r1 = tools.error_result(e)
        info = make_log_info(u'同步蓝鲸用户', u'业务日志', u'user_info', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
        mess = "同步失败"
    add_log(info)
    return mess


def get_user_type(user_name):
    """
    获取用户角色字段
    :param request:
    :return:
    """
    user_type = user_info.objects.filter(user_name=user_name)
    for i in user_type:
        user_type = i.user_type_id
    return user_type
