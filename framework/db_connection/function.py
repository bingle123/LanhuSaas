# -*- coding: utf-8 -*-
from __future__ import division
import json
from django.forms.models import model_to_dict
from db_connection.models import *
from shell_app import tools
import pymysql as MySQLdb
import base64
import pyDes
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from monitor_item.models import *
from celery.task import periodic_task
import datetime
import sys
from logmanagement.function import add_log, make_log_info
from conf import settings_development, default, settings_production, settings_testing
from position.models import *

Key = "YjCFCmtd"
Iv = "yJXYwjYD"
APP_ID = default.APP_ID
APP_TOKEN = default.APP_TOKEN


def encryption_str(str):
    """
    加密
    :param str:
    :return:
    """
    password = str.encode(encoding='utf-8')
    method = pyDes.des(Key, pyDes.CBC, Iv, pad=None, padmode=pyDes.PAD_PKCS5)
    # 执行加密码
    k = method.encrypt(password)
    # 转base64编码并返回
    return base64.b64encode(k)


def decrypt_str(data):
    """
    解密
    :param data:
    :return:
    """
    password = data.encode(encoding='utf-8')
    method = pyDes.des(Key, pyDes.CBC, Iv, pad=None, padmode=pyDes.PAD_PKCS5)
    # 对base64编码解码
    k = base64.b64decode(password)
    # 再执行Des解密并返回
    return method.decrypt(k)


def selecthor(request):
    """
    数据库链接模糊查询
    :param request:
    :return:
    """
    result_dict = dict()
    list_set = list()
    res = json.loads(request.body)
    search = res['search'].strip()
    page = res['page']
    limit = res['limit']
    # 如果搜索内容为空，搜索所有
    if None is not search and '' != search:
        sciencenews = Conn.objects.filter(
            Q(connname__contains=search) | Q(type__contains=search) | Q(ip__contains=search) \
            | Q(port__contains=search) | Q(username__contains=search) | Q(databasename__contains=search))
    else:
        sciencenews = Conn.objects.all()
    # 将数据分页
    p = Paginator(sciencenews, limit)
    try:
        selected_set = p.page(page)  # 获取第page页的数据
    except EmptyPage:
        selected_set = p.page(p.num_pages)
    for selected_data in selected_set:
        conn = model_to_dict(selected_data)
        password = conn['password']
        conn['password'] = decrypt_str(password)
        list_set.append(conn)
    # 返回页码内容
    result_dict['items'] = list_set
    # 返回总页数
    result_dict['pages'] = p.num_pages
    return result_dict


def saveconn_all(request):
    """
    保存
    :param request:
    :return:
    """
    try:
        res = json.loads(request.body)
        cilent = tools.interface_param(request)
        user = cilent.bk_login.get_user({})
        # 获取用户名
        res['createname'] = request.user.username
        res['editname'] = request.user.username

        # 密码加密后保存
        password = encryption_str(res['password'])
        res['password'] = password
        re = Conn(**res).save()
        status_dic = {}
        # 计算总页数，取5有余就+1页
        items_count = Conn.objects.count()
        pages = items_count / 5
        if 0 != items_count % 5:
            pages = pages + 1
        status_dic['message'] = 'ok'
        status_dic['page_count'] = pages

        info = make_log_info(u'增加数据库连接配置', u'业务日志', u'Conn', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
        add_log(info)
        return tools.success_result(status_dic)
    except Exception as e:
        info = make_log_info(u'增加数据库连接配置', u'业务日志', u'Conn', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
        add_log(info)
        res1 = tools.error_result(e)
        return res1


def editconn(request):
    """
    修改
    :param request:
    :return:
    """
    try:
        # 拿到当前用户，保存为修改人
        res = json.loads(request.body)
        res['editname'] = request.user.username
        res['edittime'] = datetime.datetime.now()
        # 点修改密码进行解密
        password = encryption_str(res['password'])
        res['password'] = password
        re1 = Conn.objects.filter(id=res['id']).update(**res)
        info = make_log_info(u'修改数据库连接配置', u'业务日志', u'Conn', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
        add_log(info)
        return tools.success_result(re1)
    except Exception as e:
        res1 = tools.error_result(e)
        info = make_log_info(u'修改数据库连接配置', u'业务日志', u'Conn', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
        add_log(info)
        return res1


def delete_conn(request, id):
    """
    删除
    :param request:
    :param id:
    :return:
    """
    try:
        res = Conn.objects.filter(id=id).delete()
        info = make_log_info(u'删除数据库连接配置', u'业务日志', u'Conn', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
        add_log(info)
        status_dic = {}
        # 删除完后重新计算页数
        items_count = Conn.objects.count()
        pages = items_count / 5
        if 0 != items_count % 5:
            pages = pages + 1
        status_dic['message'] = 'ok'
        status_dic['page_count'] = pages
        return tools.success_result(status_dic)
    except Exception as e:
        res1 = tools.error_result(e)
        info = make_log_info(u'删除数据库连接配置', u'业务日志', u'Conn', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
        add_log(info)
        return tools.error_result(res1)


def get_conname(request):
    """
    根据id获取数据库连接配置并返回
    :param request:
    :return:
    """
    try:
        res = request.body
        res_obj = Conn.objects.get(id=res)
        conn = model_to_dict(res_obj)
        reslut = tools.success_result(conn)
    except Exception as e:
        reslut = tools.error_result(e)
    return reslut


def testConn(request):
    """
    测试
    :param request:
    :return:
    """
    res = json.loads(request.body)
    ip = str(res['ip'])
    port = res['port']
    username = res['username']
    password = res['password']
    databasename = res['databasename']
    try:
        if res['type'] == 'MySQL':
            db = MySQLdb.connect(host=ip, user=username, passwd=password, db=databasename, port=int(port))
        elif res['type'] == 'Oracle':
            sql = r'%s/%s@%s/%s' % (username, password, ip, databasename)
            # db = cx_Oracle.connect(sql)
            db = None
        else:
            # SqlServer数据库链接包暂时有部署问题，暂时取消该功能
            # db = pymssql.connect(host=ip + r':' + port, user=username, password=password, database=databasename)
            return tools.error_result("暂不支持SqlServer类型数据库！")
        cursor = db.cursor()
        if cursor != '':
            cursor.close()
            db.close()
            return tools.success_result('0')
    except Exception as e:
        return tools.error_result(e)


def get_all_db_connection(request):
    """
    获取所有的数据库名称
    :param request:
    :return:
    """
    try:
        conn = Conn.objects.all()
        result = []
        for con in conn:
            obj = model_to_dict(con)
            result.append(obj)
        return tools.success_result(result)
    except Exception as e:
        return tools.error_result(str(e))


def get_jobInstance(request):
    """
    获取作业状态以及作业步骤状态
    :param request:
    :return:
    """
    monitor = Monitor.objects.filter(status=0, monitor_type=3)
    jion_list = []
    dic = []
    for moni in monitor:
        jobId = model_to_dict(moni)['jion_id']
        jion_list.append(jobId)
    for jion in jion_list:
        try:
            job_ins = Job.objects.filter(job_id=jion)
            for y in job_ins:
                cilent = tools.interface_param(request)
                id = y.instance_id
                instance_status = cilent.job.get_job_instance_status({
                    "bk_app_code": APP_ID,
                    "bk_app_secret": APP_TOKEN,
                    "bk_biz_id": 2,
                    "job_instance_id": id,
                })
                # 作业状态码
                iStatus = instance_status['data']['job_instance']['status']
                # 作业步骤状态码
                stepStatus = instance_status['data']['blocks'][0]['step_instances'][0]['status']
                dic.append(iStatus)
                dic.append(stepStatus)
            return dic
        except Exception as e:
            return e


def get_flowStatus(request):
    """
    获取流程节点状态并实时更新
    :param request:
    :return:
    """
    try:
        flow = Monitor.objects.filter(status=0, monitor_type=4)  # 流程元类型
        flow_list = []
        dic = []
        for x in flow:
            flow_list.append(model_to_dict(x)['jion_id'])
        for y in flow_list:
            flows = Flow.objects.filter(flow_id=y)
            for i in flows:
                cilent = tools.interface_param(request)
                res = cilent.sops.get_task_status({
                    "bk_app_code": APP_ID,
                    "bk_app_secret": APP_TOKEN,
                    "bk_biz_id": "2",
                    "task_id": y,  # task_id
                })
                res1 = cilent.sops.create_task({
                    "bk_app_code": APP_ID,
                    "bk_app_secret": APP_TOKEN,
                    "bk_biz_id": "2",
                    "template_id": "5",
                    "name": "zz",
                    "flow_type": "common"
                })
                task_id = res1['data']['task_id']
                time = datetime.datetime.now()
                # 创建节点
                Flow.objects.create(instance_id=task_id, status=0, start_time=None, test_flag=1, flow_id=y)
                status = 0
                if res['data']['state'] == 'RUNNING':
                    status = 2
                    r = Flow.objects.filter(instance_id=task_id).update(status=status, start_time=time)
                elif res['data']['state'] == 'FAILED':
                    status = 3
                elif res['data']['state'] == 'SUSPENDED':
                    status = 4
                elif res['data']['state'] == 'REVOKED':
                    status = 5
                elif res['data']['state'] == 'FINISHED':
                    status = 6
        info = make_log_info(u'增加节点', u'业务日志', u'Flow', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
    except Exception as e:
        info = make_log_info(u'增加节点', u'业务日志', u'Flow', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
    add_log(info)
    r = Flow.objects.filter(instance_id=task_id).update(status=status)
    return r


def selecthor2(request):
    """
    菜单模糊查询
    :param request:
    :return:
    """
    res = json.loads(request.body)
    result_dict = dict()
    list_set = list()
    search = res['search'].strip()
    page = res['page']
    limit = res['limit']
    if None is not search and '' != search:
        sciencenews = Muenu.objects.filter(Q(mname__contains=search) | Q(url__contains=search)).exclude(
            url='db_connection/muenu_manage/')
    else:
        sciencenews = Muenu.objects.all().exclude(url='db_connection/muenu_manage/')
    p = Paginator(sciencenews, limit)

    try:
        selected_set = p.page(page)  # 获取第page页的数据
    except EmptyPage:
        selected_set = p.page(p.num_pages)
    for selected_data in selected_set:
        menus = model_to_dict(selected_data)
        list_set.append(menus)
    result_dict['items'] = list_set
    result_dict['pages'] = p.num_pages
    return result_dict


def get_user_muenu(request):
    """
    获取角色对应的菜单名和Url
    :param request:
    :return:
    """
    cilent = tools.interface_param(request)
    # 蓝鲸平台获取当前用户，取得当前用户的角色id
    # user = cilent.bk_login.get_user({})
    # bk_roleid = user['data']['bk_role']
    # 根据菜单和角色表查出该角色对应的菜单
    user_dto_name = request.user.username
    user_db = user_info.objects.filter(user_name=user_dto_name)
    role_id = 1
    if user_db.count() > 0:
        user_db_data = user_db.get()
        role_id = user_db_data.user_pos_id
    role_menus = rm.objects.filter(roleid=role_id)
    temp_list = []
    for r_m in role_menus:
        # 菜单id，菜单表和菜单角色表都要对应起来
        menu_id = model_to_dict(r_m)['muenuid']
        # 菜单名称
        menu_name = Muenu.objects.get(id=menu_id)
        temp = {}
        temp = model_to_dict(menu_name)
        temp_list.append(temp)
    return tools.success_result(temp_list)


def addmuenus(request):
    """
    增加菜单
    :param request:
    :return:
    """
    try:
        status_dic = {}
        res = json.loads(request.body)
        re = Muenu(**res).save()
        items_count = Muenu.objects.count()
        # 增加菜单后重新查看总页数
        pages = items_count / 5
        if 0 != items_count % 5:
            pages = pages + 1
        status_dic['message'] = 'ok'
        status_dic['page_count'] = pages

        info = make_log_info(u'增加菜单', u'业务日志', u'Muenu', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
        add_log(info)
        return tools.success_result(status_dic)
    except Exception as e:
        res1 = tools.error_result(e)
        info = make_log_info(u'增加菜单', u'业务日志', u'Muenu', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
        add_log(info)
        return res1


def edit_muenu(request):
    """
    修改菜单
    :param request:
    :return:
    """
    try:
        res = json.loads(request.body)
        re1 = Muenu.objects.filter(id=res['id']).update(**res)
        info = make_log_info(u'修改菜单', u'业务日志', u'Muenu', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
        add_log(info)
        return tools.success_result(re1)
    except Exception as e:
        res1 = tools.error_result(e)
        info = make_log_info(u'修改菜单', u'业务日志', u'Muenu', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
        add_log(info)
        return res1


def delete_muenu(request, id):
    """
    删除菜单
    :param request:
    :param id:
    :return:
    """
    # 先删除菜单，再删除该菜单下的所有角色，两表无外键Id
    try:
        Muenu.objects.get(id=id).delete()
        rm.objects.filter(muenuid=id).all().delete()
        info = make_log_info(u'删除菜单', u'业务日志', u'Muenu', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
        add_log(info)
        info = make_log_info(u'删除菜单', u'业务日志', u'rm', sys._getframe().f_code.co_name,
                             request.user.username, '成功', '无')
        add_log(info)
        return tools.success_result(None)
    except Exception as e:
        info = make_log_info(u'删除菜单', u'业务日志', u'Muenu', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
        add_log(info)
        info = make_log_info(u'删除菜单', u'业务日志', u'rm', sys._getframe().f_code.co_name,
                             request.user.username, '失败', repr(e))
        add_log(info)
        res3 = tools.error_result(e)
        return tools.error_result(res3)


def get_roleAmuenus(request):
    """
    获取角色下面的菜单
    :param request:
    :return:
    """
    roles = Role.objects.all()
    menus = Muenu.objects.all()
    tree = []
    for role in roles:
        treeItem = {}
        # 获取所有菜单
        muenu_ids = rm.objects.filter(roleid=role.id)
        # 菜单名称
        treeItem['label'] = role.rname
        # 每个菜单对应的id
        treeItem['id'] = role.id
        # 二级目录都是菜单
        childrens = []
        for menu in menus:
            child = {}
            # 树对应的Id,以及label,经过处理的树id不重复
            child['id'] = (role.id + 1) * 1000 + menu.id
            child['label'] = menu.mname
            childrens.append(child)
        # 返回树的数据
        treeItem['children'] = childrens
        tree.append(treeItem)
    return tree


def checked_menu(request):
    """
    获取勾选ID
    :param request:
    :return:
    """
    # 中间表
    rm_all = rm.objects.all()
    ids = []
    for rl in rm_all:
        # 获取经过处理的树Id
        temp_id = (rl.roleid + 1) * 1000 + rl.muenuid
        ids.append(temp_id)
    print ids
    return ids


def savemnus(request):
    """
    更新角色菜单权限
    :param request:
    :return:
    """
    ids = json.loads(request.body)
    # 保留角色菜单中间表
    rm_all = rm.objects.all()
    r_all = rm_all
    x = 0
    z = 0
    parent_id = []
    son_id = []
    # 获取拿到数据第一个值，如果为数字型数组，则权限未发生变动
    if isinstance(ids[0], int):
        return 1
    # 如果获取的是对象数组，则变动了
    else:
        # 保存角色菜单前先删除中间表，中间表不为空则删除
        if rm_all is not None:
            de = rm.objects.all().delete()
            try:
                for id in ids:
                    if ('children' not in id) and ('label' in id):
                        # 逐个树id还原成菜单id(之前经过处理 树id = (角色id+1)*100+菜单Id)
                        x = id['id'] // 1000
                        z = id['id'] % 1000
                        x = int(x)
                        res1 = rm.objects.create(roleid=x - 1, muenuid=z)
                    else:
                        pass
                info = make_log_info(u'逐条增加菜单与角色中间表', u'业务日志', u'rm', sys._getframe().f_code.co_name,
                                     request.user.username, '成功', '无')
                add_log(info)
            except Exception as e:
                for i in r_all:
                    rm.objects.create(roleid=model_to_dict(i)['roleid'], muenuid=model_to_dict(i)['muenuid'])
                info = make_log_info(u'逐条增加菜单与角色中间表', u'业务日志', u'rm', sys._getframe().f_code.co_name,
                                     request.user.username, '失败', repr(e))
                add_log(info)
                return tools.error_result(e)


def get_db():
    """
    获得数据库连接对象
    :return:
    """
    if default.RUN_MODE == 'PRODUCT':
        res = settings_production.DATABASES['default']
    elif default.RUN_MODE == 'TEST':
        res = settings_testing.DATABASES['default']
    else:
        res = settings_development.DATABASES['default']
    db = MySQLdb.connect(res['HOST'], res['USER'], res['PASSWORD'], res['NAME'], charset='utf8')
    return db


def getAny_db(id):
    """
    通用数据库连接对象
    :param id:
    :return:
    """
    res = Conn.objects.get(id=id)
    conn = model_to_dict(res)
    ip = str(conn['ip'])
    port = conn['port']
    username = conn['username']
    password = decrypt_str(conn['password'])
    databasename = conn['databasename']
    if conn['type'] == 'MySQL':
        db = MySQLdb.connect(host=ip, user=username, passwd=password, db=databasename, port=int(port), charset='utf8')
    elif conn['type'] == 'Oracle':
        sql = r'%s/%s@%s/%s' % (username, password, ip, databasename, 'charset=utf8')
        # db = cx_Oracle.connect(sql)
        db = None
    else:
        # SqlServer数据库链接包暂时有部署问题，暂时取消该功能
        # db = pymssql.connect(host=ip + r':' + port, user=username, password=password, database=databasename,
        #                      charset='utf8')
        db = None
    return db

def get_all_mImgs():
    '''
    获取所有的图标
    :return:
    '''
    muenus = Muenu.objects.filter(~Q(mImg=""))
    mImgs=[]
    for i in range(len(muenus)):
        mImgs.append({'value':muenus[i].mImg})
    return mImgs
