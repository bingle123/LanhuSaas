# -*- coding: utf-8 -*-
from __future__ import division

from gatherDataHistory.models import TDGatherHistory
from logmanagement.models import *
from django.core.paginator import *
from db_connection.function import get_db
from monitor_item.models import Scene_monitor, Monitor
from system_config.function import *
from notification.models import *
from monitorScene.models import *
from monitor_item import tools
from monitor_item import models
from monitor_item.models import Scene_monitor,Monitor,Job
from conf import settings_development
import MySQLdb
import time
from datetime import datetime,date,timedelta
from gatherData.models import TDGatherData
from gatherDataHistory.models import TDGatherHistory
from market_day.models import Holiday

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
        print res3,res4
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
    print sql
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
    print res['date_Choice']
    if(res['date_Choice']):
        res3 = res['date_Choice'][0]
        res4 = res['date_Choice'][1]
    res_list = []
    tmp = Operatelog.objects.all()          #查询所有的表信息

    #if组合判断查询的数据
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
        log = tmp.filter(Q(log_type__icontains=res1) & (Q(log_name__icontains=res2) | Q(user_name__icontains=res2) | Q(
            class_name__icontains=res2) | Q(method__icontains=res2)))
    elif (res1 != "" and res2 != ""and res3!="" and res4!=""):
        print 567
        log = tmp.filter((Q(log_type__icontains=res1)) & (Q(log_name__icontains=res2) | Q(user_name__icontains=res2) | Q(
            class_name__icontains=res2) | Q(method__icontains=res2))& (Q(create_time__range=(res3,res4))))
    elif(res3!="" and res4!="" and res1!="" and res2 == ""):
        print 111
        log = tmp.filter(Q(log_type__icontains=res1) & Q(create_time__range=(res3, res4)))
    elif(res3!="" and res4!="" and res2!="" and res1 == ""):
        log = tmp.filter((Q(log_name__icontains=res2) | Q(user_name__icontains=res2) | Q(
        class_name__icontains=res2) | Q(method__icontains=res2))& Q(create_time__range=(res3, res4)))
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
    keyword = res1['keyword'].strip()      #关键字搜索
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
def getPant_list(scene_list,d_data,all_itemid,count):
    last_list = []
    AllList = []
    new_AllList = []


    for s in scene_list:
        AllList.append(str(s[0]).split(' ')[0])
    print AllList
    for All in AllList:
        if All not in new_AllList:
            new_AllList.append(All)
    #循环去重之后的日期,
    print new_AllList
    for l in new_AllList:
        success_items = 0
        failed_items = 0
        alertNums = 0
        itemNums = 0
        for x in d_data:
            if str(x).split(' ')[0] == l:
                failed_items += 1

        for y in AllList:
            if l == y:
                itemNums = itemNums +1
        print itemNums,failed_items
        success_items = itemNums - failed_items
        be_list = []
        #取得当日一个场景下的时间最小值和最大值
        for i in all_itemid:
            ts = TDGatherHistory.objects.filter(item_id=i)
            for t in ts:
                tds = model_to_dict(t)
                tds['gather_time'] = t.gather_time
                if str(tds['gather_time']).split(' ')[0] == l:
                    be_list.append(tds['gather_time'])
        mx = max(be_list)
        mi = min(be_list)
        time_consum = mx - mi
        time_consum = str(time_consum)
        alog = TdAlertLog.objects.filter(item_id=i)
        #告警数
        for al in alog:
            alertlog = model_to_dict(al)
            alertlog['alert_time'] = al.alert_time
            if str(alertlog['alert_time']).split(' ')[0] ==l:
                alertNums +=1
        persent = (success_items/itemNums) *100
        mx = str(mx)
        mi = str(mi)
        dic_data = {
            'timedata':l,
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
    if count > 7:
        last_list = last_list[0:7]
        return tools.success_result(last_list)
    else:
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

    # 根据开始结束时间查询单个场景下所有监控项每一天最后一个采集到的数据
    all_itemid = []
    # 所有监控项,字符串拼接
    str1 = ""
    for i in sm:
        all_itemid.append(model_to_dict(i)['item_id'])
    for i, index in enumerate(all_itemid):
        if (i + 1) < all_itemid.__len__():
            str1 = str(index) + ","
        else:
            str1 += str(index)
    try:
        sql = "SELECT * from (select max(a.gather_time) AS mtime,a.item_id " \
              "FROM (SELECT  t.* FROM (SELECT  DATE_FORMAT(tt.gather_time, '%Y-%m-%d') AS xx," \
              "tt.gather_time,tt.gather_error_log,tt.item_id	" \
              "FROM td_gather_history tt WHERE	item_id IN (" + str1 + ")) AS t WHERE   " \
            "gather_time BETWEEN '" + b_time + "'  AND '" + e_time + "' ORDER BY item_id,gather_time) a	group by " \
            "a.item_id,a.xx)  as m ORDER BY m.mtime"
        DATABASES = settings_development.DATABASES['default']
        db = MySQLdb.connect(host=DATABASES['HOST'], user=DATABASES['USER'], passwd=DATABASES['PASSWORD'],
                             db=DATABASES['NAME'], charset="utf8")
        cursor = db.cursor()
        cursor.execute(sql)
        res1 = cursor.fetchall()
    except Exception as e:
        return tools.error_result(e)
    scene_list = list(res1)
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
    Alldays = (datetime.strptime(e_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(b_time, "%Y-%m-%d %H:%M:%S")).days
    # 间隔天数小于3不查，大于3但是查到的有效天数小于3也不要
    if Alldays < 3:
        return tools.success_result(Alldays)
    else:
        if count < 3:
            return tools.success_result(Alldays)
        # 有效天大于3天小于7天，取所有天数
        elif count >= 3 and count <= 7:
            return getPant_list(scene_list, d_data, all_itemid, count)
        # 有效期大于7天，取前7天，splen为取数组中的前7天个数
        else:
            splen = item_len * 7 - 1
            scene_list = scene_list[:splen]
            return getPant_list(scene_list, d_data, all_itemid, count)





#场景运行情况
def select_scene_operation():
    #初始化
    res_list = []
    date_info = []
    failed_num = 0
    #获取第一个场景创建的日期
    strat_time = Scene.objects.all().first().scene_creator_time
    strat_time = strat_time.strftime("%Y-%m-%d")
    now = datetime.now().date()
    oneday = timedelta(days=1)
    yester_day = now
    while strat_time <= str(yester_day):
        date_info.append(yester_day)
        yester_day -= oneday
    #获取对应日期的所有场景
    for i in date_info:
        #初始化
        failed_num = 0
        scene_num = 0
        scenes = []
        temp = str(i)+' 23:59:59'
        sql = "SELECT * from tb_monitor_scene where scene_creator_time < '" + temp + "'"
        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql)
        scenes_list = cursor.fetchall()
        for j in scenes_list:
            scenes.append(j[0])
            flag = 1
            #判断是否为本场景是否在交易日
            scene_area_id = j[8]
            if check_jobday(scene_area_id,i):
                #获取场景所对应的所有监控项id
                items = Scene_monitor.objects.filter(scene_id=j[0])
                #判断每个监控项的运行结果是成功还是失败
                for k in items:
                    item = Monitor.objects.get(id = k.item_id)
                    if u'基本单元类型' == item.monitor_type:
                        if 'sql' == item.gather_params:
                            temp = TDGatherData.objects.get(item_id=item.id,data_key='DB_CONNECTION')
                            if temp.gather_time.strftime("%Y-%m-%d") == i:
                                if temp.gather_error_log:
                                    flag = 0
                            else:
                                temp = TDGatherHistory.objects.filter(item_id=item.id,data_key='DB_CONNECTION').last()
                                if temp.gather_error_log:
                                    flag = 0
                        if 'file' == item.gather_params:
                            temp = TDGatherData.objects.get(item_id=item.id,data_key='FILE_EXIST')
                            if temp.gather_time.strftime("%Y-%m-%d") == i:
                                if temp.gather_error_log:
                                    flag = 0
                            else:
                                temp = TDGatherHistory.objects.filter(item_id=item.id,data_key='FILE_EXIST').last()
                                if temp.gather_error_log:
                                    flag = 0
                        if 'interface' == item.gather_params:
                            temp = TDGatherData.objects.get(item_id=item.id,data_key='URL_CONNECTION')
                            if temp.gather_time.strftime("%Y-%m-%d") == i:
                                if temp.gather_error_log:
                                    flag = 0
                            else:
                                temp = TDGatherHistory.objects.filter(item_id=item.id,data_key='URL_CONNECTION').last()
                                if temp.gather_error_log:
                                    flag = 0
                    if u'作业单元类型' == item.monitor_type:
                        temp = TDGatherData.objects.get(item_id=item.id)
                        if temp.gather_time.strftime("%Y-%m-%d") == i:
                            if temp.gather_error_log:
                                flag = 0
                        else:
                            temp = TDGatherHistory.objects.filter(item_id=item.id).last()
                            if temp.gather_error_log:
                                flag = 0
                    if u'流程单元类型' == item.monitor_type:
                        temp = TDGatherHistory.objects.filter(item_id=item.id)
                        for l in temp:
                            if l.gather_error_log:
                                flag = 0
                                break
                    if u'图表单元类型' == item.monitor_type:
                        temp = TDGatherData.objects.get(item_id=item.id, data_key='DB_CONNECTION')
                        if temp.gather_time.strftime("%Y-%m-%d") == i:
                            if temp.gather_error_log:
                                flag = 0
                        else:
                            temp = TDGatherHistory.objects.filter(item_id=item.id, data_key='DB_CONNECTION').last()
                            if temp.gather_error_log:
                                flag = 0
                if flag == 0:
                    failed_num += 1
                #场景总数
                scene_num += 1
        #成功数
        success_num = scene_num - failed_num
        #成功率
        if scene_num != 0:
            success_rate = round(success_num/scene_num,4)
            success_rate = str(success_rate*100)+'%'
        #获取告警数目
        temp2 = str(i) + '%'
        sql2 = "SELECT count(*) from td_alert_log WHERE alert_time like " + "'"+ temp2 + "'"
        cursor = db.cursor()
        cursor.execute(sql2)
        alert_num = cursor.fetchall()[0][0]
        #alert = TdAlertLog.objects.filter(Q(alert_time__icontains= i))
        #alert_num = len(alert)
        dict = {
            'date':str(i),
            'scene_num':scene_num,
            'success_num':success_num,
            'success_rate':success_rate,
            'failed_num':failed_num,
            'alert_num':alert_num
        }
        #非交易日剔除
        if scene_num != 0:
            res_list.append(dict)
    return  res_list

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

#运行情况分页
def operation_page(request):
    res = json.loads(request.body)
    res_list = []
    limit = res['limit']
    page = res['page']
    scene_operation = select_scene_operation()
    p = Paginator(scene_operation, limit)
    count = p.page_range
    pages = count[-1]
    current_page = p.page(page)
    for x in current_page.object_list:
        temp_dict = {
            'page_count': pages
        }
        x = dict(x, **temp_dict)
        res_list.append(x)
    return res_list

#周运行情况
def get_week(request):
    scene_operation = select_scene_operation()
    res = json.loads(request.body)
    #初始化

    days = []
    res_list = []
    #获取一周的第一天
    res['date'] = str(res['date'])[:10]
    temp = datetime.strptime(res['date'], "%Y-%m-%d")
    date = datetime.date(temp)
    days.append(date)
    #加6天
    oneday = timedelta(days=1)
    for i in range(6):
        date += oneday
        days.append(date)
    for j in days:
        for k in scene_operation:
            if str(j) == k['date']:
                res_list.append(k)
    return res_list


def monthly_select(request):
    res = select_scene_operation()
    total = 0
    Success_num=0
    failure_num = 0
    dic_list=[]
    for i in res:
        if(str(i['date'])[5:7] == '01'):
            total += i['scene_num']
            Success_num += i['success_num']
            failure_num +=i['failed_num']
        elif(str(i['date'])[5:7] == '02'):
            total += i['scene_num']
            Success_num += i['success_num']
            failure_num += i['failed_num']
        elif (str(i['date'])[5:7] == '03'):
            total += i['scene_num']
            Success_num += i['success_num']
            failure_num += i['failed_num']
        elif (str(i['date'])[5:7] == '04'):
            total += i['scene_num']
            Success_num += i['success_num']
            failure_num += i['failed_num']
        elif (str(i['date'])[5:7] == '05'):
            total += i['scene_num']
            Success_num += i['success_num']
            failure_num += i['failed_num']
        elif (str(i['date'])[5:7] == '06'):
            total += i['scene_num']
            Success_num += i['success_num']
            failure_num += i['failed_num']
        elif (str(i['date'])[5:7] == '07'):
            total += i['scene_num']
            Success_num += i['success_num']
            failure_num += i['failed_num']
        elif (str(i['date'])[5:7] == '08'):
            total += i['scene_num']
            Success_num += i['success_num']
            failure_num += i['failed_num']
        elif (str(i['date'])[5:7] == '09'):
            total += i['scene_num']
            Success_num += i['success_num']
            failure_num += i['failed_num']
        elif (str(i['date'])[5:7] == '10'):
            total += i['scene_num']
            Success_num += i['success_num']
            failure_num += i['failed_num']
        elif (str(i['date'])[5:7] == '11'):
            total += i['scene_num']
            Success_num += i['success_num']
            failure_num += i['failed_num']
        elif (str(i['date'])[5:7] == '12'):
            total += i['scene_num']
            Success_num += i['success_num']
            failure_num += i['failed_num']
    if(str(i['date'])[:7] == '2019-01'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic={
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'date':'2019-01'
        }
        dic_list.append(dic)
    elif(str(i['date'][:7]) == '2019-02'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'date': '2019-02'
        }
        dic_list.append(dic)
    elif(str(i['date'][:7]) == '2019-03'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'date': '2019-03'
        }
        dic_list.append(dic)
    elif(str(i['date'][:7]) == '2019-04'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'date': '2019-04'
        }
        dic_list.append(dic)
    elif(str(i['date'][:7]) == '2019-05'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'date': '2019-05'
        }
        dic_list.append(dic)
    elif(str(i['date'][:7]) == '2019-06'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'date': '2019-06'
        }
        dic_list.append(dic)
    elif(str(i['date'][:7]) == '2019-07'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'date': '2019-07'
        }
        dic_list.append(dic)
    elif(str(i['date'][:7]) == '2019-08'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'date': '2019-08'
        }
        dic_list.append(dic)
    elif(str(i['date'][:7]) == '2019-09'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'date': '2019-09'
        }
        dic_list.append(dic)
    elif(str(i['date'][:7]) == '2019-10'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'date': '2019-10'
        }
        dic_list.append(dic)
    elif(str(i['date'][:7]) == '2019-11'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'date': '2019-11'
        }
        dic_list.append(dic)
    elif(str(i['date'][:7]) == '2019-12'):
        success_rate = round(Success_num / total, 4)
        success_rate = str(success_rate * 100) + '%'
        dic = {
            'total':total,
            'Success_num':Success_num,
            'failure_num':failure_num,
            'success_rate':success_rate,
            'date': '2019-12'
        }

        dic_list.append(dic)
    return dic_list