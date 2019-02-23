# -*- coding: utf-8 -*-
from __future__ import division
import json
import time
from django.forms.models import model_to_dict
from db_connection.models import *
from shell_app import tools
import pymysql as MySQLdb
import cx_Oracle
import pymssql
import datetime
import base64
import pyDes
from django.db.models import Q
from django.core.paginator import Paginator
from monitor.models import *
from celery.task import periodic_task
import datetime
import sys
from logmanagement.function import add_log,make_log_info,get_active_user

Key = "YjCFCmtd"
Iv = "yJXYwjYD"
#加密
def encryption_str(str):
    password = str.encode(encoding='utf-8')
    method = pyDes.des(Key, pyDes.CBC, Iv, pad=None, padmode=pyDes.PAD_PKCS5)
    # 执行加密码
    k = method.encrypt(password)
    # 转base64编码并返回
    return base64.b64encode(k)


#解密
def decrypt_str(data):
    password = data.encode(encoding='utf-8')
    method = pyDes.des(Key, pyDes.CBC, Iv, pad=None, padmode=pyDes.PAD_PKCS5)
    # 对base64编码解码
    k = base64.b64decode(password)
    # 再执行Des解密并返回
    return method.decrypt(k)


#数据库链接模糊查询
def selecthor(request):
    res = json.loads(request.body)
    search = res['search']
    page = res['page']
    limit = res['limit']
    sciencenews = Conn.objects.filter(Q(connname__contains=search)|Q(type__contains=search)|Q(ip__contains=search)\
                                      |Q(port__contains=search)|Q(username__contains=search)|Q(databasename__contains=search))
    p = Paginator(sciencenews, limit)
    count = p.page_range
    pages = count[-1]

    curren_page = p.page(page)
    objs = []
    for cur in curren_page.object_list:
        conn = model_to_dict(cur)
        conn['count'] = pages
        password = conn['password']
        conn['password'] = decrypt_str(password)
        objs.append(conn)
    return objs

# 查询所有
def getconn_all(request):
    res = json.loads(request.body)
    page = res['page']
    limit = res['limit']
    conn = Conn.objects.all()
    p = Paginator(conn, limit)
    count = p.page_range
    pages = count[-1]
    objs=[]
    current_page = p.page(page)
    for cur in current_page.object_list:
        conn=model_to_dict(cur)
        conn['count'] = pages
        password = conn['password']
        conn['password'] = decrypt_str(password)
        objs.append(conn)
    return objs


# 保存
def saveconn_all(request):
    # try:
        res = json.loads(request.body)
        cilent = tools.interface_param(request)
        user = cilent.bk_login.get_user({})
        res['createname'] = user['data']['bk_username']
        res['editname'] = user['data']['bk_username']

        password = encryption_str(res['password'])
        res['password'] = password
        re = Conn(**res).save()
        status_dic = {}
        res = json.loads(request.body)
        items_count = Conn.objects.count()
        pages = items_count / 5
        if 0 != items_count % 5:
            pages = pages + 1
        status_dic['message'] = 'ok'
        status_dic['page_count'] = pages

        info = make_log_info(u'保存数据库连接配置', u'业务日志', u'Conn', sys._getframe().f_code.co_name, get_active_user(request)['data']['bk_username'],'成功','无')
        add_log(info)
        return tools.success_result(status_dic)
    # except Exception as e:
    #     info = make_log_info(u'保存数据库连接配置', u'业务日志', u'Conn', sys._getframe().f_code.co_name, get_active_user(request)['data']['bk_username'],'失败',repr(e))
    #     add_log(info)
    #     res1 = tools.error_result(e)
    #     print e
    #     return res1


#修改
def eidtconnn(request):
    try:
        res = json.loads(request.body)
        res.pop('count')
        cilent = tools.interface_param(request)
        user = cilent.bk_login.get_user({})
        res['editname'] = user['data']['bk_username']
        res['edittime'] = datetime.datetime.now()

        password = encryption_str(res['password'])
        res['password'] = password
        re1 = Conn.objects.filter(id=res['id']).update(**res)
        info = make_log_info(u'修改数据库连接配置', u'业务日志', u'Conn', sys._getframe().f_code.co_name,get_active_user(request)['data']['bk_username'], '成功', '无')
        add_log(info)
        return tools.success_result(re1)
    except Exception as e:
        res1 = tools.error_result(e)
        info = make_log_info(u'修改数据库连接配置', u'业务日志', u'Conn', sys._getframe().f_code.co_name,get_active_user(request)['data']['bk_username'], '失败', repr(e))
        add_log(info)
        return res1


# 删除
def delete_conn(request,id):
    try:
        res = Conn.objects.filter(id=id).delete()
        info = make_log_info(u'删除数据库连接配置', u'业务日志', u'Conn', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '成功', '无')
        add_log(info)
        return tools.success_result(res)
    except Exception as e:
        res1 = tools.error_result(e)
        info = make_log_info(u'删除数据库连接配置', u'业务日志', u'Conn', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '失败', repr(e))
        add_log(info)
        return tools.error_result(res1)


# 获取名称
def get_conname(request):
    try:
        res = request.body
        res_obj = Conn.objects.get(id=res)
        conn = model_to_dict(res_obj)
        reslut =  tools.success_result(conn)
    except Exception as e:
        reslut = tools.error_result(e)
    return reslut


# 测试
def testConn(request):
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
            sql = r'%s/%s@%s/%s'%(username, password, ip, databasename)
            db = cx_Oracle.connect(sql)
        else:
            db = pymssql.connect(host=ip+r':'+port, user=username, password=password, database=databasename)
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
        res = Conn.objects.all()
        result = []
        for i in res:
            obj = model_to_dict(i)
            result.append(obj)
        return tools.success_result(result)
    except Exception as e:
        return tools.error_result(str(e))

#获取作业状态以及作业步骤状态
def get_jobInstance(request):
    monitor = Monitor.objects.filter(status=0, monitor_type='作业单元类型')
    jion_list = []
    dic = []
    for x in monitor:
        jobId = model_to_dict(x)['jion_id']
        jion_list.append(jobId)
    for i in jion_list:
        try:
            job_ins = Job.objects.filter(job_id=i)
            for y in job_ins:
                cilent = tools.interface_param(request)
                id = y.instance_id
                instance_status = cilent.job.get_job_instance_status({
                    "bk_app_code": "mydjango1",
                    "bk_app_secret": "99d97ec5-4864-4716-a877-455a6a8cf9ef",
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


# 获取流程节点状态并实时更新
@periodic_task(run_every=5)
def get_flowStatus(request):
    flow = Monitor.objects.filter(status=0, monitor_type='流程元类型')
    flow_list = []
    dic = []
    for x in flow:
        flow_list.append(model_to_dict(x)['jion_id'])
    for y in flow_list:
        flows = Flow.objects.filter(flow_id=y)
        for i in flows:

            cilent = tools.interface_param(request)
            res = cilent.sops.get_task_status({
                "bk_app_code": "mydjango1",
                "bk_app_secret": "99d97ec5-4864-4716-a877-455a6a8cf9ef",
                "bk_biz_id": "2",
                "task_id": y,  # task_id
            })
            res1 = cilent.sops.create_task({
                "bk_app_code": "mydjango1",
                "bk_app_secret": "99d97ec5-4864-4716-a877-455a6a8cf9ef",
                "bk_biz_id": "2",
                "template_id": "5",
                "name": "zz",
                "flow_type": "common"
            })
            task_id = res1['data']['task_id']
            time = datetime.datetime.now()
            #创建节点
            Flow.objects.create(instance_id=task_id, status=0, start_time=None, test_flag=1, flow_id=y)
            status = 0
            if res['data']['state'] == 'RUNNING':
                status = 2
                r = Flow.objects.filter(instance_id=task_id).update(status=status,start_time=time)
            elif res['data']['state'] == 'FAILED':
                status = 3
            elif res['data']['state'] == 'SUSPENDED':
                status = 4
            elif res['data']['state'] == 'REVOKED':
                status = 5
            elif res['data']['state'] == 'FINISHED':
                status = 6

            r = Flow.objects.filter(instance_id=task_id).update(status=status)
            return r


############################菜单#########################

#菜单模糊查询
def selecthor2(request):
    res = json.loads(request.body)
    search = res['search']
    page = res['page']
    limit = res['limit']
    sciencenews = Muenu.objects.filter(Q(mname__contains=search)|Q(url__contains=search)).exclude(url ='db_connection/muenu_manage/')
    p = Paginator(sciencenews, limit)
    count = p.page_range
    pages = count[-1]

    curren_page = p.page(page)
    objs = []
    for cur in curren_page.object_list:
        muenu = model_to_dict(cur)
        muenu['count'] = pages
        objs.append(muenu)
    return objs

#获取角色对应的菜单名和Url
def get_user_muenu(request):
    cilent = tools.interface_param(request)
    user = cilent.bk_login.get_user({})
    bk_roleid = user['data']['bk_role']
    role_muenus = rm.objects.filter(roleid=bk_roleid)
    temp_list = []
    for i in role_muenus:
        muenuid = model_to_dict(i)['muenuid']
        muenu = Muenu.objects.get(id=muenuid)
        temp = {}
        temp = model_to_dict(muenu)
        temp_list.append(temp)
    return tools.success_result(temp_list)






#获取所有菜单
def get_all_muenu(request):
    res = json.loads(request.body)
    page = res['page']
    limit = res['limit']
    muenus = Muenu.objects.all().exclude(url ='db_connection/muenu_manage/')
    p = Paginator(muenus, limit)
    count = p.page_range
    pages = count[-1]
    objs = []
    current_page = p.page(page)
    for cur in current_page.object_list:
        muenus = model_to_dict(cur)
        muenus['count'] = pages
        objs.append(muenus)
    return objs




#增加菜单
def addmuenus(request):
    try:
        status_dic ={}
        res = json.loads(request.body)
        re = Muenu(**res).save()
        items_count = Muenu.objects.count()
        pages = items_count / 5
        if 0 != items_count % 5:
            pages = pages + 1
        status_dic['message'] = 'ok'
        status_dic['page_count'] = pages

        info = make_log_info(u'增加菜单', u'业务日志', u'Muenu', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '成功', '无')
        add_log(info)
        return tools.success_result(status_dic)
    except Exception as e:
        res1 = tools.error_result(e)
        info = make_log_info(u'增加菜单', u'业务日志', u'Muenu', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'],'失败',repr(e))
        add_log(info)
        return res1



#修改菜单
def edit_muenu(request):
    try:
        res = json.loads(request.body)
        res.pop('count')
        re1 = Muenu.objects.filter(id=res['id']).update(**res)
        info = make_log_info(u'修改菜单', u'业务日志', u'Muenu', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '成功', '无')
        add_log(info)
        return tools.success_result(re1)
    except Exception as e:
        res1 = tools.error_result(e)
        info = make_log_info(u'修改菜单', u'业务日志', u'Muenu', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '失败', repr(e))
        add_log(info)
        return res1


#删除菜单
def delete_muenu(request,id):
    try:
        res1 = Muenu.objects.get(id=id).delete()
        res2 = rm.objects.get(muenuid=id).delete()
        info = make_log_info(u'删除菜单', u'业务日志', u'Muenu', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '成功', '无')
        add_log(info)
        info = make_log_info(u'删除菜单', u'业务日志', u'rm', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '成功', '无')
        add_log(info)
        if res1 !=None & res2 !=None:
            return tools.success_result(res1)
    except Exception as e:
        info = make_log_info(u'删除菜单', u'业务日志', u'Muenu', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '失败', repr(e))
        add_log(info)
        info = make_log_info(u'删除菜单', u'业务日志', u'rm', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '失败', repr(e))
        add_log(info)
        res3 = tools.error_result(e)
        return tools.error_result(res3)

def get_roleAmuenus(request):
    roles = Role.objects.all()
    menus = Muenu.objects.all()
    tree=[]
    for x in roles:
        temp = {}
        muenu_ids = rm.objects.filter(roleid=x.id)
        temp['label']=x.rname
        temp['id']=x.id
        childrens=[]
        for menu in menus:
            chi={}
            chi['id']=(x.id)*50+menu.id
            chi['label']=menu.mname
            childrens.append(chi)
        temp['children']=childrens
        tree.append(temp)
    return tree

#获取已经勾选Id
def checked_menu(request):
    objs=rm.objects.all()
    roles = Role.objects.all()
    rolelen = roles.__len__()
    menus = Muenu.objects.all()
    menuslen = menus.__len__()
    ids=[]
    for obj in objs:
        temp_id=(obj.roleid)*50+obj.muenuid
        ids.append(temp_id)
    return  ids


#获取所有节点菜单
def savemnus(request):
    ids = json.loads(request.body)
    print ids[1:]
    res = rm.objects.all()
    ms = res
    x = 0
    z = 0
    parent_id = []
    son_id = []
    if isinstance(ids[0],int):
        return 1
    else:
        if res is not None:
            de = rm.objects.all().delete()
            try:
                for i in ids:
                    if ('children' not in i) and ('label' in i):
                        x = i['id'] / 50
                        z = i['id'] % 50
                        x = int(x)
                        res1 = rm.objects.create(roleid=x, muenuid=z)
                    else:
                        pass
            except Exception as e:
                for i in ms:
                    rm.objects.create(roleid=model_to_dict(i)['roleid'],muenuid=model_to_dict(i)['muenuid'])
                return tools.error_result(e)

