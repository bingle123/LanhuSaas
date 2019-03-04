# -*- coding: utf-8 -*-
from __future__ import division
from logmanagement.models import *
from django.core.paginator import *
from system_config.function import *
from notification.models import *
from monitorScene.models import *
from monitor_item import tools
from conf import settings_development
import MySQLdb
def show_all(request):
    """
        显示所有操作日志
    """
    res = json.loads(request.body)
    limit = res['limit']
    page = res['page']
    log = Operatelog.objects.all()
    p = Paginator(log, limit)
    count = p.page_range
    pages = count[-1]
    res_list = []
    current_page = p.page(page)
    for x in current_page:
        dic = {
            'id': x.id,
            'log_type': x.log_type,
            'log_name': x.log_name,
            'user_name': x.user_name,
            'class_name': x.class_name,
            'method': x.method,
            'create_time': str(x.create_time),
            'succeed': x.succeed,
            'message': x.message,
            'page_count': pages
        }
        res_list.append(dic)
    return  res_list


def select_all_rules(request):
    res1 = json.loads(request.body)
    limit = res1['limit']
    page = res1['page']
    DATABASES = settings_development.DATABASES['default']
    db = MySQLdb.connect(host=DATABASES['HOST'], user=DATABASES['USER'], passwd=DATABASES['PASSWORD'], db=DATABASES['NAME'],charset="utf8")
    cursor = db.cursor()
    cursor.execute("select distinct e.scene_id,e.id,e.monitor_name,e.scene_name,f.alert_title,f.alert_content,f.alert_time,f.persons "
                   "FROM(SELECT c.scene_id,c.item_id,c.scene_name,d.id,d.monitor_name "
                   "FROM(SELECT DISTINCT b.scene_id, a.scene_name, b.item_id "
                   "FROM tb_monitor_scene AS a, tl_scene_monitor AS b "
                   "WHERE a.id = b.scene_id ) AS c, tb_monitor_item AS d "
                   "WHERE c.item_id = d.id ) AS e, td_alert_log AS f "
                   "WHERE e.item_id = f.item_id ORDER BY e.scene_name")
    res = cursor.fetchall()
    p = Paginator(res, limit)
    count = p.page_range
    pages = count
    res_list = []
    current_page = p.page(page)
    res_list = list(current_page)
    res_list2 = []
    for i in range(0,len(res_list)):
        dic={
            'scene_id':res_list[i][0],
            'id':res_list[i][1],
            'monitor_name': res_list[i][2],
            'scene_name':res_list[i][3],
            'alert_title':res_list[i][4],
            'alert_content':res_list[i][5],
            'alert_time':str(res_list[i][6]),
            'persons':res_list[i][7],
            'pages':len(pages)
        }
        res_list2.append(dic)
    db.close()
    res2 = tools.success_result(res_list2)
    return res2


# 分页获取告警规则
def select_rules_pagination(request):
    res1 = json.loads(request.body)
    limit = res1['limit']
    page = res1['page']
    search = res1['search'].strip()
    print (search)
    if(search):
        print 456
        DATABASES = settings_development.DATABASES['default']
        db = MySQLdb.connect(host=DATABASES['HOST'], user=DATABASES['USER'], passwd=DATABASES['PASSWORD'],
                             db=DATABASES['NAME'], charset="utf8")
        cursor = db.cursor()
        cursor.execute(
            "select distinct e.scene_id,e.id,e.monitor_name,e.scene_name,f.alert_title,f.alert_content,f.alert_time,f.persons "
            "FROM(SELECT c.scene_id,c.item_id,c.scene_name,d.id,d.monitor_name "
            "FROM(SELECT DISTINCT b.scene_id, a.scene_name, b.item_id "
            "FROM tb_monitor_scene AS a, tl_scene_monitor AS b "
            "WHERE a.id = b.scene_id ) AS c, tb_monitor_item AS d "
            "WHERE c.item_id = d.id ) AS e, td_alert_log AS f "
            "WHERE e.item_id = f.item_id and  e.scene_name = '" + search + "'"
                                                                           " ORDER BY e.scene_name")
        res = cursor.fetchall()
    else:
        print 123
        DATABASES = settings_development.DATABASES['default']
        db = MySQLdb.connect(host=DATABASES['HOST'], user=DATABASES['USER'], passwd=DATABASES['PASSWORD'],
                             db=DATABASES['NAME'], charset="utf8")
        cursor = db.cursor()
        cursor.execute(
            "select distinct e.scene_id,e.id,e.monitor_name,e.scene_name,f.alert_title,f.alert_content,f.alert_time,f.persons "
            "FROM(SELECT c.scene_id,c.item_id,c.scene_name,d.id,d.monitor_name "
            "FROM(SELECT DISTINCT b.scene_id, a.scene_name, b.item_id "
            "FROM tb_monitor_scene AS a, tl_scene_monitor AS b "
            "WHERE a.id = b.scene_id ) AS c, tb_monitor_item AS d "
            "WHERE c.item_id = d.id ) AS e, td_alert_log AS f "
            "WHERE e.item_id = f.item_id ORDER BY e.scene_name")
        res = cursor.fetchall()
    p = Paginator(res, limit)
    count = p.page_range
    pages = count
    res_list = []
    current_page = p.page(page)
    res_list = list(current_page)
    res_list2 = []
    for i in range(0, len(res_list)):
        dic = {
            'scene_id': res_list[i][0],
            'id': res_list[i][1],
            'monitor_name': res_list[i][2],
            'scene_name': res_list[i][3],
            'alert_title': res_list[i][4],
            'alert_content': res_list[i][5],
            'alert_time': str(res_list[i][6]),
            'persons': res_list[i][7],
            'pages': len(pages)
        }
        res_list2.append(dic)
    db.close()
    res2 = tools.success_result(res_list2)
    return res2

# def select_Keyword(request):
#     res = json.loads(request.body)
#     limit = res['limit']
#     page = res['page']
#     search = res['search'].strip()
#     res1 = search
#     res_list = []
#     tmp = Operatelog.objects.all()
#     log = tmp.filter(Q(log_type__icontains=res1) | Q(log_name__icontains=res1) | Q(user_name__icontains=res1) | Q(
#         class_name__icontains=res1) | Q(method__icontains=res1))
#     p = Paginator(log, limit)
#     count = p.page_range
#     pages = count[-1]
#     current_page = p.page(page)
#     for x in current_page:
#         dic = {
#             'id': x.id,
#             'log_type': x.log_type,
#             'log_name': x.log_name,
#             'user_name': x.user_name,
#             'class_name': x.class_name,
#             'method': x.method,
#             'create_time': str(x.create_time),
#             'succeed': x.succeed,
#             'message': x.message,
#             'page_count': pages
#         }
#         res_list.append(dic)
#     return res_list

def select_log(request):
    res = json.loads(request.body)
    limit = res['limit']
    page = res['page']
    search = res['search'].strip()
    res1 = search
    res2 = res['keyword']
    res3 = ""
    res4 = ""
    print res['date_Choice']
    if(res['date_Choice']):
        res3 = res['date_Choice'][0]
        res4 = res['date_Choice'][1]
    res_list = []
    tmp = Operatelog.objects.all()
    if(res1 != ""and res2 == "" and res3 == "" and res4 == ""):
        print 123
        log = tmp.filter(Q(log_type__icontains=res1))
    elif(res2 != "" and res1 == "" and res3 == "" and res4 == ""):
        print 234
        log = tmp.filter(Q(log_name__icontains=res2) | Q(user_name__icontains=res2) | Q(
        class_name__icontains=res2) | Q(method__icontains=res2))
    elif(res3 != ""and res1 == "" and res2 == ""):
        print 345
        log = tmp.filter(Q(create_time__range=(res3,res4)))
    elif(res1 != "" and res2 != "" and res3 == "" and res4 ==""):
        print 456
        log = tmp.filter(Q(log_type__icontains=res1) and Q(log_name__icontains=res2) | Q(user_name__icontains=res2) | Q(
            class_name__icontains=res2) | Q(method__icontains=res2))
    elif (res1 != "" and res2 != ""and res3!="" and res4!=""):
        print 567
        log = tmp.filter(Q(log_type__icontains=res1) and Q(log_name__icontains=res2) | Q(user_name__icontains=res2) | Q(
            class_name__icontains=res2) | Q(method__icontains=res2)and Q(create_time__range=(res3,res4)))
    elif(res3!="" and res4!="" and res1!="" and res2 == ""):
        print 111
        log = tmp.filter(Q(log_type__icontains=res1)and Q(create_time__range=(res3, res4)))
    elif(res3!="" and res4!="" and res2!="" and res1 == ""):
        log = tmp.filter(Q(log_name__icontains=res2) | Q(user_name__icontains=res2) | Q(
        class_name__icontains=res2) | Q(method__icontains=res2)and Q(create_time__range=(res3, res4)))
    elif(res1 == ""and res2 == "" and res3 == "" and res4 == ""):
        log = Operatelog.objects.all()
    p = Paginator(log, limit)
    count = p.page_range
    pages = count[-1]
    current_page = p.page(page)
    for x in current_page:
        dic = {
            'id': x.id,
            'log_type': x.log_type,
            'log_name': x.log_name,
            'user_name': x.user_name,
            'class_name': x.class_name,
            'method': x.method,
            'create_time': str(x.create_time),
            'succeed': x.succeed,
            'message': x.message,
            'page_count': pages
        }
        res_list.append(dic)
    return res_list
