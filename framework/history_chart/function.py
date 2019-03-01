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


def select_all_rules():
    DATABASES = settings_development.DATABASES['default']
    db = MySQLdb.connect(host=DATABASES['HOST'], user=DATABASES['USER'], passwd=DATABASES['PASSWORD'], db=DATABASES['NAME'],charset="utf8")
    cursor = db.cursor()
    cursor.execute("select distinct e.scene_id,e.id,e.monitor_name,e.scene_name,f.alert_title,f.alert_content,f.alert_time,f.persons "
                   "from (select c.scene_id,c.item_id,c.scene_name,d.id,d.monitor_name "
                   "from (select distinct b.scene_id,a.scene_name,b.item_id "
                   "from tb_monitor_scene  as a,tl_scene_monitor as b "
                   "where a.id = b.scene_id) as c ,tb_monitor_item as d "
                   "where c.item_id = d.id) as e, td_alert_log as f "
                   "where e.item_id = f.item_id")
    res = cursor.fetchall()
    res_list = list(res)
    res_list2 = []
    for i in range(0,len(res_list)-1):
        dic={
            'scene_id':res_list[i][0],
            'id':res_list[i][1],
            'monitor_name': res_list[i][2],
            'scene_name':res_list[i][3],
            'alert_title':res_list[i][4],
            'alert_content':res_list[i][5],
            'alert_time':str(res_list[i][6]),
            'persons':res_list[i][7],
        }
        res_list2.append(dic)
    db.close()
    res2 = tools.success_result(res_list2)
    return res2


# 分页获取告警规则
def select_rules_pagination(page_info):
    result_dict = dict()
    list_set = list()
    search = page_info['search']
    page = page_info['page']
    limit = page_info['limit']
    if None is not search and '' != search:
        rules_list = TbAlertRule.objects.filter(rule_name__contains=search).all()
    else:
        rules_list = TbAlertRule.objects.all()
    paginator = Paginator(rules_list, limit)
    try:
        selected_set = paginator.page(page)
    except PageNotAnInteger:
        selected_set = paginator.page(1)
    except EmptyPage:
        selected_set = paginator.page(paginator.num_pages)
    for selected_data in selected_set:
        create_time = selected_data.create_time
        edit_time = selected_data.edit_time
        upper_limit = selected_data.upper_limit
        lower_limit = selected_data.lower_limit
        selected_data.create_time = None
        selected_data.edit_time = None
        selected_data.upper_limit = None
        selected_data.lower_limit = None
        temp = model_to_dict(selected_data)
        if create_time is None:
            temp['create_time'] = ''
        else:
            temp['create_time'] = create_time.strftime('%Y-%m-%d %H:%M:%S')
        if edit_time is None:
            temp['edit_time'] = ''
        else:
            temp['edit_time'] = edit_time.strftime('%Y-%m-%d %H:%M:%S')
        if upper_limit is None:
            temp['upper_limit'] = ''
        else:
            temp['upper_limit'] = str(upper_limit)
        if lower_limit is None:
            temp['lower_limit'] = ''
        else:
            temp['lower_limit'] = str(lower_limit)
        list_set.append(temp)
    result_dict['items'] = list_set
    result_dict['pages'] = paginator.num_pages
    return result_dict

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
