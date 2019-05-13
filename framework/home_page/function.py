# -*- coding: utf-8 -*-

import time
import pymysql as MySQLdb
from django.forms import model_to_dict
import shell_app.tools as tools
from conf import settings_development
from gather_data_history.models import TDGatherHistory
from history_chart.function import check_jobday
from monitor_scene.models import *
from monitor_item.models import *
from notification.models import TdAlertLog
from position.models import user_info
from datetime import datetime
from models import *
from system_config.models import  *
from db_connection.function import *
from gather_data.models import TDGatherData

from monitor_item import function

def get_time(request):
    """
    获取当前时间
    :param request:
    :return:
    """
    today =  datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M")
    flag = check_jobday(1,  datetime.datetime.now())
    if flag == True:
        today_name = '交易日'
    elif flag == False:
        today_name = '非交易日'
    else:
        today_name = None
    dic_data = {
        'time_date': today,
        'today_name': today_name,
    }
    return dic_data


def scenes_alert(request):
    """
    获取当前用户所对应的岗位下的所有场景监控项的告警
    :param request:
    :return:
    """
    # 测试数据，目前写死的名字
    # 获取当前用户拿name
    user = user_info.objects.get(user_name=request.user.username)
    position_id = model_to_dict(user)['user_pos']
    # 一个职位下得所有场景
    ps = position_scene.objects.filter(position_id=position_id)
    if 0 == len(ps) or None is ps:
        null_data = 'n'
        return tools.success_result(null_data)
    alert_log = []
    # 告警数
    alert_count = 0
    alert_data = []
    all_avg = 0
    # 分别是安全。预警。危险
    safe_scene = 0
    will_scene = 0
    danger_scene = 0
    # 场景的总分值
    all_score = 0
    # 场景的错误分值
    error_score = 0
    # 多场景时的分数
    s_score = 0
    flag = 1
    for i in ps:
        # 场景id
        sid = model_to_dict(i)['scene']
        # 场景和监控项关联表
        sm = Scene_monitor.objects.filter(scene_id=sid)
        for x in sm:
            x = model_to_dict(x)
            # 循环item_id，监控项id
            x_item_id = x["item_id"]
            # 得分累加，出循环时得到总分
            scene_score = x["score"]
            print scene_score
            all_score = all_score + scene_score
            try:
                # 如果总分为0,直接为0
                gather_data = TDGatherData.objects.filter(item_id=x_item_id)
                for hi in gather_data:
                    his = model_to_dict(hi)
                    his['gather_time'] = hi.gather_time
                    if str(his['gather_time']).split(' ')[0] == time.strftime("%Y-%m-%d", time.localtime(time.time())):
                        # 如果当天时间此监控项出错，
                        if his['gather_error_log'] != None and his['gather_error_log'] != '':
                            error_score = error_score + scene_score
                        # 没有异常，正常
                        else:
                            pass

            except Exception as e:
                return tools.error_result(e)
            alert_log = TdAlertLog.objects.filter(item_id=x_item_id)
            for y in alert_log:
                alertd = model_to_dict(y)
                alertd['alert_time'] = y.alert_time
                if str(alertd['alert_time']).split(' ')[0] == time.strftime("%Y-%m-%d", time.localtime(time.time())):
                    alert_count = alert_count + 1
                    alertd['alert_time'] = str(alertd['alert_time'])
                    alert_data.append(alertd)
        # 出场景循环
        # 所有场景下得监控项得到的权值分总和/场景数 = 权值平均分 就是从健康度
        # 这是一个场景的健康度

        if all_score != 0:
            last_score = int((all_score - error_score) * 100 / all_score)
        else:
            last_score = 0
        if flag > 1:
            s_score =int((s_score + last_score)/2)
        else:
            s_score = last_score
        flag = flag + 1
        # 按场景判断
        if s_score == 100:
            safe_scene = safe_scene + 1
        elif s_score < 100 and all_score > 90:
            will_scene = will_scene + 1
        else:
            danger_scene = danger_scene + 1

    dic_data = {
        'alert_count': alert_count,  # 告警数
        'last_score': s_score,  # 健康度
        'safe_scene': safe_scene,
        'will_scene': will_scene,
        'danger_scene': danger_scene,
    }
    return dic_data


def query_alert_data():
    """
    告警数据
    :return:
    """
    data = AlertInfo.objects.all()
    if data.count() > 0:
      #  res_data = data.values_list()
        if len(data) > 0:
            res = []
            for dto in data:
                temp = model_to_dict(dto)
                if dto.alert_time !=None:
                    temp["alert_time"] = dto.alert_time.strftime('%Y-%m-%d %H:%M:%S')
                if dto.modify_time !=None:
                    temp["modify_time"] = dto.modify_time.strftime('%Y-%m-%d %H:%M:%S')
                res.append(temp)
            return res;
    return None


def query_curr_sences(request):
    """
    查询所有场景分组
    :param request:
    :return:
    """
    data_db = SceneType.objects.all()
    res = []
    if len(data_db)>0:
        for dto in data_db:
            vo = model_to_dict(dto)
            if dto.create_time != None:
               vo["create_time"] = dto.create_time.strftime('%Y-%m-%d %H:%M:%S')
            if dto.update_time != None:
                vo["update_time"] = dto.update_time.strftime('%Y-%m-%d %H:%M:%S')
            if dto.start_time != None:
                vo["start_time"] = dto.start_time.strftime('%H:%M:%S')
            if dto.stop_time != None:
                vo["stop_time"] = dto.stop_time.strftime('%H:%M:%S')
            res.append(vo)
    return res
    # user = user_info.objects.get(user_name=request.user.username)
    # position_id = model_to_dict(user)['user_pos']
    # # 一个职位下得所有场景
    # ps = position_scene.objects.filter(position_id=position_id)
    #
    # sence_data_list = []
    # if  len(ps):
    #     for dto in ps:
    #         dt = Scene.objects.filter(id=dto.scene_id)
    #         if dt.count()>0:
    #             temp = dt.get()
    #             vo = model_to_dict(temp)
    #             if temp.scene_creator_time != None:
    #                 vo["scene_creator_time"] = temp.scene_creator_time.strftime('%Y-%m-%d %H:%M:%S')
    #             if temp.scene_editor_time != None:
    #                 vo["edit_creator_time"] = temp.scene_editor_time.strftime('%Y-%m-%d %H:%M:%S')
    #             if temp.scene_startTime != None:
    #                 vo["scene_startTime"] = temp.scene_startTime.strftime('%Y-%m-%d %H:%M:%S')
    #             if temp.scene_endTime != None:
    #                 vo["scene_endTime"] = temp.scene_endTime.strftime('%Y-%m-%d %H:%M:%S')
    #             sence_data_list.append(vo)
    #         # dt = Scene_monitor
    # return sence_data_list;


def scenes_item_list(request):
   '''
   场景类型查询监控
   :param request:
   :return:
   '''
   #监控项类型 0 正在执行 1 异常  2 提醒 3未执行
   item_type = request.POST.get("item_type")
   scene_type = request.POST.get("scene_type")
   start_time =request.POST.get("startTime")
   stop_time = request.POST.get("stopTime")

   #查询场景
   sql_str =" SELECT	a.id AS scene_id,a.scene_name AS scene_name,c.id,c.monitor_name AS scene_node," \
            " c.start_time,c.end_time, " \
            " CASE WHEN TIMESTAMPDIFF(MINUTE,c.start_time,CURRENT_TIME ) > 0" \
            "            AND TIMESTAMPDIFF( MINUTE 	,c.end_time,CURRENT_TIME) < 0 " \
            "      THEN " \
            "      ( " \
            "        CASE WHEN c.score IS NULL	OR d.score IS NULL " \
            "                 OR c.score != d.score " \
            "             THEN '异常'" \
            "             ELSE  (" \
            "                     CASE WHEN TIMESTAMPDIFF(MINUTE,CURRENT_TIME,c.end_time) <= 30" \
            "                               AND TIMESTAMPDIFF(MINUTE,CURRENT_TIME,c.end_time) > 0 " \
            "                          THEN  '提醒' " \
            "                          ELSE  '正在执行'     " \
            "                      END  " \
            "                    )     " \
            "         END     " \
            "     ) " \
            "     ELSE '未执行'" \
            " END" \
            " FROM tb_monitor_scene a " \
            " JOIN tl_scene_monitor b ON a.id = b.scene_id "
   if scene_type != None:
       sql_str=sql_str+" AND a.scene_type_id = '"+scene_type.decode('utf-8').encode('gb18030') +"' "
   if start_time!=None:
       sql_str=sql_str+"  AND a.scene_startTime >= '"+start_time.decode('utf-8').encode('gb18030') +"' "
   if stop_time!=None:
       sql_str=sql_str+" AND a.scene_endTime <= '"+stop_time.decode('utf-8').encode('gb18030') +"' "

   sql_str = sql_str+" JOIN tb_monitor_item c ON b.item_id = c.id " \
            "  JOIN td_gather_data d ON b.item_id = d.item_id"
   db = get_db()
   cursor = db.cursor()
   cursor.execute(sql_str)
   res = cursor.fetchall()
   cursor.close()
   res_data=[]
   if len(res) > 0:
       map={} # 0 正在执行 1 异常  2 提醒 3未执行
       map["0"]="正在执行"
       map["1"] = "异常"
       map["2"] = "提醒"
       map["3"] = "未执行"
       for dto_db in res:
           if dto_db[6].encode("utf-8") != map.get(item_type)\
              and map.get(item_type) != None:
              continue
           dt ={}
           dt["scene_id"] = dto_db[0]
           dt["scene_name"] = dto_db[1]
           dt["item_id"]  = dto_db[2]
           dt["scene_node"] = dto_db[3]
           dt["start_time"] = str(dto_db[4])
           dt["end_time"] = str(dto_db[5])
           dt["scene_status"] = dto_db[6]
           res_data.append(dt)
   return res_data

    # scenes_id = request.POST.get("scenes_id")
    # data_list = Monitor.objects.filter(scene_id=scenes_id)
    # scene_dto = Scene.objects.filter(scene_id= scenes_id).get()
    # if data_list.count()>0:
    #     for dto in data_list:
    #         dt = model_to_dict(dto)
    #         res_dto = {}
    #         res_dto["scene_id"] = scene_dto.scene_name
    #         res_dto["scene_id"] = scene_dto.scene_id
    #         res_dto["scene_node"] = dt.get("monitor_name")
    #         res_dto["start_time"] = "";
    #         res_dto["end_time"] = "";
    #         res_dto["scene_status"]

#   张美庆 2019-5-11
#   在界面展示各系统运行情况
def select_All():
    result = function.select_all();
    print 'zheshifanhuizhi'
    print result;
    #dict = ['1']
    return result