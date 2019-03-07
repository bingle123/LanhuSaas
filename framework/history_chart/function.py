# -*- coding: utf-8 -*-
from __future__ import division

from gatherDataHistory.models import TDGatherHistory
from logmanagement.models import *
from django.core.paginator import *

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
        sql = sql+"and  e.scene_name = '" + search + "'"\

    if(keyword):
        sql=sql+"and (e.scene_id = '" + keyword + "' or e.id ='" + keyword + "' or e.monitor_name = '" + keyword + "' or f.alert_title='" + keyword + "' or f.alert_content='" + keyword + "' or f.alert_time='" + keyword + "' or f.persons='" + keyword + "') "\

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

def about_search(request):
    res1 = json.loads(request.body)
    print res1
    limit = res1['limit']
    page = res1['page']
    search = res1['search'].strip()
    keyword = res1['keyword'].strip()
    res3 = ""
    res4 = ""
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
    if(search):
        sql = sql+" and e.scene_name = '"+search+"'"
    if(keyword):
        sql = sql+" and (e.scene_id='"+keyword+"' or e.item_id='"+keyword+"' or e.monitor_name='"+keyword+"')"
    if(res1['date_Choice']):
        sql = sql+" and e.start_time between '"+res3+"' and '"+res4+"'"
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

#场景对比分析
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


#计算天数
def Caltime(date1,date2):

    #%Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
    date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
    # date1=time.strptime(date1,"%Y-%m-%d")
    # date2=time.strptime(date2,"%Y-%m-%d")
    #根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
    date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
    # date1=datetime.datetime(date1[0],date1[1],date1[2])
    # date2=datetime.datetime(date2[0],date2[1],date2[2])
    #返回两个变量相差的值，就是相差天数
    return date2-date1

def selectScenes_ById(request):
    res = json.loads(request.body)
    scene = Scene.objects.get(id = res['id'])
    #根据id查监控项个数
    sm = Scene_monitor.objects.filter(scene_id=res['id'])
    item_len = sm.__len__()
    b_time = res['dataTime'][0]
    e_time = res['dataTime'][1]
    itemNums = 0
    success_items = 0
    failed_items = 0

    all_itemid = []
    str1 = ""
    for i in sm:
        all_itemid.append(model_to_dict(i)['item_id'])
    for i,index in enumerate(all_itemid):
        if (i+1) < all_itemid.__len__():
            str1 = str(index)+","
        else:
            str1 += str(index)
    itemNums = all_itemid.__len__()


    sql = "SELECT * from (select max(a.gather_time) AS mtime,a.item_id FROM (SELECT  t.* FROM (SELECT  DATE_FORMAT(tt.gather_time, '%Y-%m-%d') AS xx,tt.gather_time,tt.gather_error_log,tt.item_id	FROM td_gather_history tt WHERE	item_id IN ("+str1+")) AS t WHERE   gather_time BETWEEN '"+b_time+"'  AND '"+e_time+"' ORDER BY item_id,gather_time) a	group by a.item_id,a.xx)  as m ORDER BY m.mtime"

    DATABASES = settings_development.DATABASES['default']
    db = MySQLdb.connect(host=DATABASES['HOST'], user=DATABASES['USER'], passwd=DATABASES['PASSWORD'],
                         db=DATABASES['NAME'], charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    res1 = cursor.fetchall()
    scene_list = []
    scene_list = list(res1)
    d_data = []
    for i in scene_list:
        h = TDGatherHistory.objects.get(gather_time=i[0],item_id=i[1])
        if model_to_dict(h)['gather_error_log'] != '' and  model_to_dict(h)['gather_error_log'] != None:
            d_data.append(i[0])
        else:
            pass
    print d_data
    #得到的
    scene_list_len = scene_list.__len__()

    #查到的总天数
    listCount_date = scene_list_len/item_len

    #时间间隔数
    Alldays = (datetime.strptime(e_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(b_time, "%Y-%m-%d %H:%M:%S")).days


    if Alldays < 3:
        return tools.error_result(Alldays)
    elif Alldays >=3 and Alldays<=7:
        if listCount_date < 3:
            return tools.error_result(Alldays)
        else:
            print 'qnmlgb'
    else:
        if listCount_date < 3:
            return tools.error_result(Alldays)
        elif listCount_date >= 3 and listCount_date <=7:
            print 'laileladi'
            last_list = []
            AllList = []
            for s in scene_list:
                AllList.append(str(s[0]).split(' ')[0])
            AllList = list(set(AllList))
            for l in AllList:
                success_items = 0
                failed_items = 0
                itemNums = 0
                for x in d_data:
                    if str(x).split(' ')[0] == l:
                        failed_items += 1
                success_items = all_itemid.__len__() - failed_items
                itemNums = all_itemid.__len__()
                dic_data = {
                    'timedata':l,
                    'success_items':success_items,
                    'failed_items':failed_items,
                    'itemNums':itemNums,
                }
                last_list.append(dic_data)
            return tools.success_result(last_list)
        else:
            splen = item_len*7
            print scene_list[:splen]









    # dic_data = {
    #     'compare_date':'',
    #     'scene_startTime': model_to_dict(scene)['scene_startTime'],
    #     'scene_endTime': model_to_dict(scene)['scene_endTime'],
    #     'itemNums':itemNums,
    #     'count_time':'',
    #     'success_items':'',
    #     'success_percent':'',
    #     'failed_percent':'',
    #     'alertNums':'',
    # }

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
        scenes = []
        scenes_list = Scene.objects.filter(Q(scene_creator_time__lt=i))
        scenes_list2 = Scene.objects.filter(Q(scene_creator_time__icontains=i))
        scenes_list=scenes_list|scenes_list2
        for j in scenes_list:
            scenes.append(j.id)
            flag = 1
            flag2 = 0
            #判断是否为交易日
            scene_area_id = j.scene_area
            if check_jobday(scene_area_id,i):
                flag2 = 1
            #获取场景所对应的所有监控项id
            items = Scene_monitor.objects.filter(scene_id=j.id)
            #判断每个监控项的运行结果是成功还是失败
            for k in items:
                print k.item_id
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
        scene_num = len(scenes)
        #成功数
        success_num = scene_num - failed_num
        #成功率
        success_rate = round(success_num/scene_num,4)
        success_rate = str(success_rate*100)+'%'
        #获取告警数目
        alert = TdAlertLog.objects.filter(Q(alert_time__icontains= i))
        alert_num = len(alert)
        dict = {
            'date':str(i),
            'scene_num':scene_num,
            'success_num':success_num,
            'success_rate':success_rate,
            'failed_num':failed_num,
            'alert_num':alert_num
        }
        #非交易日剔除
        if flag2:
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
    for i in res:
        total += i['scene_num']
    print total
    print res