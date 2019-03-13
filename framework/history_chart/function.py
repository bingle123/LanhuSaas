# -*- coding: utf-8 -*-
from __future__ import division

from gather_data_history.models import TDGatherHistory
from logmanagement.models import *
from django.core.paginator import *
from db_connection.function import get_db
from system_config.function import *
from notification.models import *
from monitor_scene.models import *
from monitor_item import tools
from monitor_item import models
from monitor_item.models import Scene_monitor,Monitor,Job
from conf import settings_development
import MySQLdb
import time
from datetime import datetime,date,timedelta
from gather_data.models import TDGatherData
from gather_data_history.models import TDGatherHistory
from market_day.models import Holiday
from models import operation_report

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

#搜索分页的首页table
def select_all_rules(request):
    res1 = json.loads(request.body)
    limit = res1['limit']
    page = res1['page']
    #数据库的连接配置
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
    #对sql语句的返回结果进行分页
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
    keyword = res1['keyword'].strip()
    date_Choice =res1['date_Choice']
    if(res1['date_Choice']):
        res3 = res1['date_Choice'][0]
        res4 = res1['date_Choice'][1]
    DATABASES = settings_development.DATABASES['default']
    db = MySQLdb.connect(host=DATABASES['HOST'], user=DATABASES['USER'], passwd=DATABASES['PASSWORD'],
                         db=DATABASES['NAME'], charset="utf8")
    cursor = db.cursor()
    sql = "select distinct e.scene_id,e.id,e.monitor_name,e.scene_name,f.alert_title,f.alert_content,f.alert_time,f.persons "\
          "FROM(SELECT c.scene_id,c.item_id,c.scene_name,d.id,d.monitor_name "\
          "FROM(SELECT DISTINCT b.scene_id, a.scene_name, b.item_id "\
          "FROM tb_monitor_scene AS a, tl_scene_monitor AS b "\
          "WHERE a.id = b.scene_id ) AS c, tb_monitor_item AS d "\
          "WHERE c.item_id = d.id ) AS e, td_alert_log AS f "\
          "WHERE e.item_id = f.item_id "
    if(search):
        sql = sql+"and  e.scene_name LIKE '%" + search + "%'"\

    if(keyword):
        sql=sql+"and (e.scene_id LIKE '%" + keyword + "%' or e.id LIKE '%" + keyword + "%' or e.monitor_name LIKE '%" + keyword + "%' or f.alert_title LIKE '%" + keyword + "%' or f.alert_content LIKE '%" + keyword + "%' or  f.persons LIKE '%" + keyword + "%') "\

    if(date_Choice):
        sql=sql+"and f.alert_time between  '" + res3 + "'  and '" + res4 + "'"
    sql=sql+" ORDER BY e.scene_name"
    cursor.execute(sql)
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

#日志的搜索方法
def select_log(request):
    res = json.loads(request.body)
    limit = res['limit']
    page = res['page']
    search = res['search'].strip()          #场景名
    res1 = search                           #场景名
    res2 = res['keyword']                   #关键字
    res3 = ""                               #开始时间
    res4 = ""                               #结束时间
    if(res['date_Choice']):
        res3 = res['date_Choice'][0]
        res4 = res['date_Choice'][1]
    res_list = []
    tmp = Operatelog.objects.all()          #查询所有的表信息

    #if组合判断查询的数据
    if(res1 != ""and res2 == "" and res3 == "" and res4 == ""):
        log = tmp.filter(Q(log_type__icontains=res1))
    elif(res2 != "" and res1 == "" and res3 == "" and res4 == ""):
        log = tmp.filter(Q(log_name__icontains=res2) | Q(user_name__icontains=res2) | Q(
        class_name__icontains=res2) | Q(method__icontains=res2) |Q(succeed__icontains=res2))
    elif(res3 != ""and res1 == "" and res2 == ""):
        log = tmp.filter(Q(create_time__range=(res3,res4)))
    elif(res1 != "" and res2 != "" and res3 == "" and res4 ==""):
        log = tmp.filter(Q(log_type__icontains=res1) & (Q(log_name__icontains=res2) | Q(user_name__icontains=res2) | Q(
            class_name__icontains=res2) | Q(method__icontains=res2)|Q(succeed__icontains=res2)))
    elif (res1 != "" and res2 != ""and res3!="" and res4!=""):
        log = tmp.filter((Q(log_type__icontains=res1)) & (Q(log_name__icontains=res2) | Q(user_name__icontains=res2) | Q(
            class_name__icontains=res2) | Q(method__icontains=res2)|Q(succeed__icontains=res2))& (Q(create_time__range=(res3,res4))))
    elif(res3!="" and res4!="" and res1!="" and res2 == ""):
        log = tmp.filter(Q(log_type__icontains=res1) & Q(create_time__range=(res3, res4)))
    elif(res3!="" and res4!="" and res2!="" and res1 == ""):
        log = tmp.filter((Q(log_name__icontains=res2) | Q(user_name__icontains=res2) | Q(
        class_name__icontains=res2) | Q(method__icontains=res2)|Q(succeed__icontains=res2))& Q(create_time__range=(res3, res4)))
    elif(res1 == ""and res2 == "" and res3 == "" and res4 == ""):
        log = Operatelog.objects.all()

    #分页
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
#即将到期table查询
def about_select(request):
    res1 = json.loads(request.body)
    limit = res1['limit']
    page = res1['page']
    sql = "select e.scene_name,e.scene_id,e.item_id,e.monitor_name,e.start_time,e.end_time,e.minture" \
          " from(SELECT round((UNIX_TIMESTAMP(now()) - UNIX_TIMESTAMP(CONCAT(DATE_FORMAT(now(),'%Y-%m-%d'),' ',d.end_time)))/60) " \
          "as minture ,d.*,c.* FROM(SELECT DISTINCT b.scene_id, a.scene_name, b.item_id  " \
          "FROM tb_monitor_scene AS a, tl_scene_monitor AS b  " \
          "WHERE a.id = b.scene_id ) AS c, tb_monitor_item AS d " \
          "WHERE c.item_id = d.id ) e;"
    DATABASES = settings_development.DATABASES['default']
    db = MySQLdb.connect(host=DATABASES['HOST'], user=DATABASES['USER'], passwd=DATABASES['PASSWORD'],
                         db=DATABASES['NAME'], charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
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
            'scene_name': res_list[i][0],
            'scene_id': res_list[i][1],
            'item_id': res_list[i][2],
            'monitor_name': res_list[i][3],
            'start_time': str(res_list[i][4]),
            'end_time': str(res_list[i][5]),
            'minture': str(res_list[i][6]),
            'pages': len(pages)
        }
        res_list2.append(dic)
    db.close()
    res2 = tools.success_result(res_list2)
    return res2

#即将到期的table条件查询
def about_search(request):
    res1 = json.loads(request.body)
    limit = res1['limit']
    page = res1['page']
    search = res1['search'].strip()     #场景名称搜索
    keyword = res1['keyword']      #关键字搜索
    res3 = ""                               #按时间搜索的开始时间
    res4 = ""                               #按时间搜索的结束时间
    if (res1['date_Choice']):
        res3 = res1['date_Choice'][0]
        res4 = res1['date_Choice'][1]
    sql = "select e.scene_name,e.scene_id,e.item_id,e.monitor_name,e.start_time,e.end_time,e.minture" \
          " from(SELECT round((UNIX_TIMESTAMP(now()) - UNIX_TIMESTAMP(CONCAT(DATE_FORMAT(now(),'%Y-%m-%d'),' ',d.end_time)))/60) " \
          "as minture ,d.*,c.* FROM(SELECT DISTINCT b.scene_id, a.scene_name, b.item_id  " \
          "FROM tb_monitor_scene AS a, tl_scene_monitor AS b  " \
          "WHERE a.id = b.scene_id ) AS c, tb_monitor_item AS d " \
          "WHERE c.item_id = d.id ) e,tb_monitor_item as l "\
           "where e.id = l.id"
    #用if组合来筛选掉不符合条件的数据
    if(search):
        sql = sql+" and e.scene_name LIKE '%"+search+"%'"
    if(keyword):
        sql = sql+" and (e.scene_id LIKE '%"+keyword+"%' or e.item_id LIKE '%"+keyword+"%' or e.monitor_name LIKE '%"+keyword+"%')"
    if(res1['date_Choice']):
        sql = sql+" and e.start_time between '"+res3+"' and '"+res4+"'"
    DATABASES = settings_development.DATABASES['default']
    db = MySQLdb.connect(host=DATABASES['HOST'], user=DATABASES['USER'], passwd=DATABASES['PASSWORD'],
                         db=DATABASES['NAME'], charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    #执行sql并分页
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
            'scene_name': res_list[i][0],
            'scene_id': res_list[i][1],
            'item_id': res_list[i][2],
            'monitor_name': res_list[i][3],
            'start_time': str(res_list[i][4]),
            'end_time': str(res_list[i][5]),
            'minture': str(res_list[i][6]),
            'pages': len(pages)
        }
        res_list2.append(dic)
    db.close()
    res2 = tools.success_result(res_list2)
    return res2

#别动
def select_scenes(request):
    #查询所有场景，遍历场景名称和id
    scenes = Scene.objects.all()
    list_data = list()
    dic_data = {}
    for i in scenes:
        dic_data = {
            'id':model_to_dict(i)['id'],
            'sname':model_to_dict(i)['scene_name'],
        }
        list_data.append(dic_data)
    return tools.success_result(list_data)

#封装方法，别动
def getPant_list(scene_list,d_data,all_itemid):
    last_list = []
    All_date = []
    new_Alldate = []

    #所有场景日期
    for scene in scene_list:
        All_date.append(str(scene[0]).split(' ')[0])
    #日期去重
    for dates in All_date:
        if dates not in new_Alldate:
            new_Alldate.append(dates)
    #循环去重之后的日期,
    for new_data in new_Alldate:
        #成功数
        success_items = 0
        #失败数
        failed_items = 0
        #告警总数
        alertNums = 0
        #单元总数
        itemNums = 0
        #遍历有错误的日期 == 去重之后有错误的日期，比对有一个就错误数+1
        for alert_data in d_data:
            if str(alert_data).split(' ')[0] == new_data:
                failed_items += 1
        for data_count in All_date:
            if new_data == data_count:
                itemNums = itemNums +1
        success_items = itemNums - failed_items
        be_list = []
        #取得当日一个场景下的时间最小值和最大值
        for itemid in all_itemid:
            ts = TDGatherHistory.objects.filter(item_id=itemid)
            for t in ts:
                tds = model_to_dict(t)
                tds['gather_time'] = t.gather_time
                if str(tds['gather_time']).split(' ')[0] == new_data:
                    be_list.append(tds['gather_time'])
        mx = max(be_list)
        mi = min(be_list)
        #时间间隔
        time_consum = mx - mi
        time_consum = str(time_consum)
        alog = TdAlertLog.objects.filter(item_id=itemid)
        #告警数
        for al in alog:
            alertlog = model_to_dict(al)
            alertlog['alert_time'] = al.alert_time
            if str(alertlog['alert_time']).split(' ')[0] ==new_data:
                alertNums +=1
        persent = (success_items/itemNums) *100
        mx = str(mx)
        mi = str(mi)
        dic_data = {
            'timedata':new_data,
            'begin_time':mi,
            'end_time':mx,
            'success_items':success_items,
            'failed_items':failed_items,
            'itemNums':itemNums,
            'alertNums':alertNums,
            'succeess_persent':persent,
            'time_consum':time_consum,
        }
        last_list.append(dic_data)
    return tools.success_result(last_list)

#场景对比分析
def selectScenes_ById(request):
    res = json.loads(request.body)
    m = Scene.objects.get(id=res['id'])
    rid = model_to_dict(m)['scene_area']
    #根据场景id查监控项个数
    sm = Scene_monitor.objects.filter(scene_id=res['id'])
    item_len = sm.__len__()
    # 获取开始结束时间
    b_time = res['dataTime'][0]
    e_time = res['dataTime'][1]
    Alldays = (datetime.strptime(e_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(b_time, "%Y-%m-%d %H:%M:%S")).days
    if Alldays > 15:
        return tools.success_result(Alldays)
    # 根据开始结束时间查询单个场景下所有监控项每一天最后一个采集到的数据
    all_itemid = []
    # 所有监控项,字符串拼接
    str1 = ""
    for scen_monitor in sm:
        all_itemid.append(model_to_dict(scen_monitor)['item_id'])
    for i, index in enumerate(all_itemid):
        if (i + 1) < all_itemid.__len__():
            str1 = str(index) + ","
        else:
            str1 += str(index)
    try:
        sql = '''SELECT * from (select max(a.gather_time) AS mtime,a.item_id 
              FROM (SELECT  t.* FROM (SELECT  DATE_FORMAT(tt.gather_time, '%Y-%m-%d') AS xx,
              tt.gather_time,tt.gather_error_log,tt.item_id	
              FROM td_gather_history tt WHERE	item_id IN (" + str1 + ")) AS t WHERE  
            gather_time BETWEEN '" + b_time + "'  AND '" + e_time + "' ORDER BY item_id,gather_time) a	group by 
            a.item_id,a.xx)  as m ORDER BY m.mtime'''
        DATABASES = settings_development.DATABASES['default']
        db = MySQLdb.connect(host=DATABASES['HOST'], user=DATABASES['USER'], passwd=DATABASES['PASSWORD'],
                             db=DATABASES['NAME'], charset="utf8")
        cursor = db.cursor()
        cursor.execute(sql)
        res1 = cursor.fetchall()
    except Exception as e:
        return tools.error_result(e)
    scene_list = list(res1)
    #所有有错误的日期
    d_data = []
    h1_new = None
    for i in scene_list:
        h = TDGatherHistory.objects.filter(item_id=i[1])
        for th in h:
            h1 = model_to_dict(th)
            h1['gather_time'] = th.gather_time
            if h1['gather_time'] == i[0]:
                h1_new = h1
                if (h1_new['gather_error_log'] != '') and (h1_new['gather_error_log'] != None):
                    d_data.append(i[0])
                else:
                    pass

    # 查到的总天数
    try:
        sql1 = "select count(*) from (select DISTINCT DATE_FORMAT(tb.mtime,'%y-%m-%d') gather_time from (SELECT * from (select max(a.gather_time) AS mtime,a.item_id FROM (SELECT  t.* FROM (SELECT  DATE_FORMAT(tt.gather_time, '%Y-%m-%d') AS xx,tt.gather_time,tt.gather_error_log,tt.item_id	FROM td_gather_history tt WHERE	item_id IN (" + str1 + ")) AS t WHERE   gather_time BETWEEN '" + b_time + "'  AND '" + e_time + "' ORDER BY item_id,gather_time) a	group by a.item_id,a.xx)  as m ORDER BY m.mtime)as tb)as tf"
        DATABASES = settings_development.DATABASES['default']
        db1 = MySQLdb.connect(host=DATABASES['HOST'], user=DATABASES['USER'], passwd=DATABASES['PASSWORD'],
                             db=DATABASES['NAME'], charset="utf8")
        cursor1 = db1.cursor()
        cursor1.execute(sql1)
        count = cursor1.fetchone()
    except Exception as e:
        return tools.error_result(e)
    count = count[0]
    # 时间间隔数

    # 间隔天数小于3不查，大于3但是查到的有效天数小于3也不要
    if Alldays < 3:
        return tools.success_result(Alldays)
    else:
        if count < 3:
            return tools.success_result(Alldays)
        # 有效天大于3天小于7天，取所有天数
        else:
            return getPant_list(scene_list, d_data, all_itemid)



#统计一天的场景运行情况
def select_scene_operation():
    # 初始化
    scenes2 = []
    failed_num = 0
    scene_num = 0
    #获取时间
    yesterday = datetime.now().date() - timedelta(days=1)
    #获取所有场景
    scenes = Scene.objects.all()
    #剔除非交易日
    for scene in scenes:
        if check_jobday(scene.scene_area,yesterday):
            scenes2.append(scene)
    #遍历所有场景
    for scene in scenes2:
        scene_monitors = Scene_monitor.objects.filter(scene_id=scene.id)
        #遍历所有监控项
        for scene_monitor in scene_monitors:
            #执行成功的状态信息，1为成功，0为失败
            flag = 1
            #根据监控项id，找到监控项
            item = Monitor.objects.get(id=scene_monitor.item_id)
            #判断是否成功
            if u'基本单元类型' == item.monitor_type:
                if 'sql' == item.gather_params:
                    temp = TDGatherData.objects.get(item_id=scene_monitor.item_id, data_key='DB_CONNECTION')
                    if temp.gather_time.strftime("%Y-%m-%d") == yesterday:
                        if temp.gather_error_log:
                            flag = 0
                    else:
                        temp = TDGatherHistory.objects.filter(item_id=scene_monitor.item_id, data_key='DB_CONNECTION').last()
                        if temp.gather_error_log:
                            flag = 0
                if 'file' == item.gather_params:
                    temp = TDGatherData.objects.get(item_id=scene_monitor.item_id, data_key='FILE_EXIST')
                    if temp.gather_time.strftime("%Y-%m-%d") == yesterday:
                        if temp.gather_error_log:
                            flag = 0
                    else:
                        temp = TDGatherHistory.objects.filter(item_id=scene_monitor.item_id, data_key='FILE_EXIST').last()
                        if temp.gather_error_log:
                            flag = 0
                if 'interface' == item.gather_params:
                    temp = TDGatherData.objects.get(item_id=scene_monitor.item_id, data_key='URL_CONNECTION')
                    if temp.gather_time.strftime("%Y-%m-%d") == yesterday:
                        if temp.gather_error_log:
                            flag = 0
                    else:
                        temp = TDGatherHistory.objects.filter(item_id=scene_monitor.item_id, data_key='URL_CONNECTION').last()
                        if temp.gather_error_log:
                            flag = 0
            if u'作业单元类型' == item.monitor_type:
                temp = TDGatherData.objects.get(item_id=scene_monitor.item_id)
                if temp.gather_time.strftime("%Y-%m-%d") == yesterday:
                    if temp.gather_error_log:
                        flag = 0
                else:
                    temp = TDGatherHistory.objects.filter(item_id=scene_monitor.item_id).last()
                    if temp.gather_error_log:
                        flag = 0
            if u'流程单元类型' == item.monitor_type:
                temp = TDGatherHistory.objects.filter(item_id=scene_monitor.item_id)
                for l in temp:
                    if l.gather_error_log:
                        flag = 0
                        break
            if u'图表单元类型' == item.monitor_type:
                temp = TDGatherData.objects.get(item_id=scene_monitor.item_id, data_key='DB_CONNECTION')
                if temp.gather_time.strftime("%Y-%m-%d") == yesterday:
                    if temp.gather_error_log:
                        flag = 0
                else:
                    temp = TDGatherHistory.objects.filter(item_id=scene_monitor.item_id, data_key='DB_CONNECTION').last()
                    if temp.gather_error_log:
                        flag = 0
        #失败数
        if flag == 0:
            failed_num += 1
        # 场景总数
        scene_num += 1
    # 成功数
    success_num = scene_num - failed_num
    # 成功率
    if scene_num != 0:
        success_rate = round(success_num / scene_num, 4)
        success_rate = str(success_rate * 100) + '%'
    else:
        success_rate = 0
    # 获取告警数目
    date = str(yesterday) + '%'
    sql = "SELECT count(*) from td_alert_log WHERE alert_time like " + "'" + date + "'"
    db = get_db()
    cursor = db.cursor()
    cursor.execute(sql)
    alert_num = cursor.fetchall()[0][0]
    db.close()
    dict = {
        'date': str(yesterday),
        'scene_num': scene_num,
        'success_num': success_num,
        'success_rate': success_rate,
        'failed_num': failed_num,
        'alert_num': alert_num
    }
    re = operation_report.objects.create(**dict)
    return  re

#显示运行情况
def show_operation_report(request):
    res = json.loads(request.body)
    res_list = []
    limit = res['limit']
    page = res['page']
    operation_reports = operation_report.objects.all()
    p = Paginator(operation_reports, limit)
    count = p.page_range
    pages = count[-1]
    current_page = p.page(page)
    for rep in current_page.object_list:
        dict = {
            'date': rep.date,
            'scene_num': rep.scene_num,
            'success_num': rep.success_num,
            'success_rate': rep.success_rate,
            'failed_num': rep.failed_num,
            'alert_num': rep.alert_num,
            'page_count': pages
        }
        res_list.append(dict)
    return res_list


#判断是否为交易日
def check_jobday(id,time):
    time=datetime(time.year,time.month,time.day)
    str_date=datetime.strftime(time,'%Y/%m/%d')
    day=str_date[:4] + u'/' + str(int(str_date[5:7])) + u'/' + str(int(str_date[8:10]))
    hs=Holiday.objects.filter(Q(day=day)&Q(area=id))
    flag=0
    for h in hs:
        flag=h.flag
    if flag==1:
        return True
    elif flag==2:
        return False


#周运行情况
def get_week(request):
    res = json.loads(request.body)
    #初始化
    res_list = []
    #获取一周的第一天
    res['date'] = str(res['date'])[:10]
    temp = datetime.strptime(res['date'], "%Y-%m-%d")
    date1 = datetime.date(temp)
    #加6天
    sixday = timedelta(days=6)
    date2 = date1 + sixday
    #获取date到date2之间的数据
    sql = "SELECT * FROM td_operation_report WHERE date between '" + str(date1) + "' and '" + str(date2) +"'"
    db = get_db()
    cursor = db.cursor()
    cursor.execute(sql)
    operation_reports = cursor.fetchall()
    for rep in operation_reports:
        dict = {
            'date': rep[1],
            'scene_num': rep[2],
            'success_num': rep[3],
            'success_rate': rep[4],
            'failed_num': rep[5],
            'alert_num': rep[6],
        }
        res_list.append(dict)
    return res_list


def monthly_select(request):
    res = operation_report.objects.all()
    total = 0
    Success_num=0
    failure_num = 0
    alert_num = 0
    dic_list=[]
    for i in res:
        if(str(i.date)[5:7] == '01'):
            total += int(i.scene_num)
            Success_num += int(i.success_num)
            failure_num += int(i.failed_num)
            alert_num += int(i.alert_num)
        elif(str(i.date)[5:7] == '02'):
            total += int(i.scene_num)
            Success_num += int(i.success_num)
            failure_num += int(i.failed_num)
            alert_num += int(i.alert_num)
        elif (str(i.date)[5:7] == '03'):
            total += int(i.scene_num)
            Success_num += int(i.success_num)
            failure_num += int(i.failed_num)
            alert_num += int(i.alert_num)
        elif (str(i.date)[5:7] == '04'):
            total += int(i.scene_num)
            Success_num += int(i.success_num)
            failure_num += int(i.failed_num)
            alert_num += int(i.alert_num)
        elif (str(i.date)[5:7] == '05'):
            total += int(i.scene_num)
            Success_num += int(i.success_num)
            failure_num += int(i.failed_num)
            alert_num += int(i.alert_num)
        elif (str(i.date)[5:7] == '06'):
            total += int(i.scene_num)
            Success_num += int(i.success_num)
            failure_num += int(i.failed_num)
            alert_num += int(i.alert_num)
        elif (str(i.date)[5:7] == '07'):
            total += int(i.scene_num)
            Success_num += int(i.success_num)
            failure_num += int(i.failed_num)
            alert_num += int(i.alert_num)
        elif (str(i.date)[5:7] == '08'):
            total += int(i.scene_num)
            Success_num += int(i.success_num)
            failure_num += int(i.failed_num)
            alert_num += int(i.alert_num)
        elif (str(i.date)[5:7] == '09'):
            total += int(i.scene_num)
            Success_num += int(i.success_num)
            failure_num += int(i.failed_num)
            alert_num += int(i.alert_num)
        elif (str(i.date)[5:7] == '10'):
            total += int(i.scene_num)
            Success_num += int(i.success_num)
            failure_num += int(i.failed_num)
            alert_num += int(i.alert_num)
        elif (str(i.date)[5:7] == '11'):
            total += int(i.scene_num)
            Success_num += int(i.success_num)
            failure_num += int(i.failed_num)
            alert_num += int(i.alert_num)
        elif (str(i.date)[5:7] == '12'):
            total += int(i.scene_num)
            Success_num += int(i.success_num)
            failure_num += int(i.failed_num)
            alert_num += int(i.alert_num)
    if(str(i.date)[:7] == str(i.date)[:5]+'01'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic={
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'alert_num':alert_num,
            'date':str(i.date)[:5]+'01'
        }
        dic_list.append(dic)
    elif(str(i.date)[:7] == str(i.date)[:5]+'02'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'alert_num':alert_num,
            'date': str(i.date)[:5]+'02'
        }
        dic_list.append(dic)
    elif(str(i.date[:7]) == str(i.date)[:5]+'03'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'alert_num':alert_num,
            'date': str(i.date)[:5]+'03'
        }
        dic_list.append(dic)
    elif(str(i.date)[:7] == str(i.date)[:5]+'04'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'alert_num':alert_num,
            'date': str(i.date)[:5]+'04'
        }
        dic_list.append(dic)
    elif(str(i.date)[:7] == str(i.date)[:5]+'05'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'alert_num':alert_num,
            'date': str(i.date)[:5]+'05'
        }
        dic_list.append(dic)
    elif(str(i.date)[:7] == str(i.date)[:5]+'06'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'alert_num':alert_num,
            'date': str(i.date)[:5]+'06'
        }
        dic_list.append(dic)
    elif(str(i.date)[:7] == str(i.date)[:5]+'07'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'alert_num':alert_num,
            'date': str(i.date)[:5]+'07'
        }
        dic_list.append(dic)
    elif(str(i.date)[:7] == str(i.date)[:5]+'08'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'alert_num':alert_num,
            'date': str(i.date)[:5]+'08'
        }
        dic_list.append(dic)
    elif(str(i.date)[:7] == str(i.date)[:5]+'09'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'alert_num':alert_num,
            'date': str(i.date)[:5]+'09'
        }
        dic_list.append(dic)
    elif(str(i.date)[:7] == str(i.date)[:5]+'10'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'alert_num':alert_num,
            'date': str(i.date)[:5]+'10'
        }
        dic_list.append(dic)
    elif(str(i.date)[:7] == str(i.date)[:5]+'11'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'alert_num':alert_num,
            'date': str(i.date)[:5]+'11'
        }
        dic_list.append(dic)
    elif(str(i.date)[:7] == str(i.date)[:5]+'12'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'alert_num':alert_num,
            'date': str(i.date)[:5]+'12'
        }

        dic_list.append(dic)
    return dic_list