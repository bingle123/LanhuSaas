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
    if flag is True:
        today_name = '交易日'
    else:
        today_name = '非交易日'
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
    # 分别是安全。预警。危险
    safe_scene = 0
    will_scene = 0
    danger_scene = 0
    # 健康度
    s_score = 0.00
    # 告警数
    alert_count = 0
    # 获取当前用户下每一个场景的监控度
    result = get_every_scene_health_degree(user.id)
    dic_data = {
        'alert_count': alert_count,  # 告警数
        'last_score': s_score,  # 健康度
        'safe_scene': safe_scene,
        'will_scene': will_scene,
        'danger_scene': danger_scene,
    }
    if result.__len__() == 0:
        return dic_data
    health_degree_total = 0.00;
    num = 0
    for scene_obj in result:
        cur_time = str(scene_obj[2]);
        start_time = str(scene_obj[3]);
        end_time = str(scene_obj[4]);
        # 正在执行的场景
        if cur_time >= start_time and cur_time <= end_time:
            health_degree_total += float(scene_obj[7]);
            num+=1
            # 第7个值为场景的得分值
            if float(scene_obj[7]) >= 90 and float(scene_obj[7]) < 100:
                will_scene += 1
                alert_count += 1
            if float(scene_obj[7]) < 90:
                danger_scene += 1
                alert_count += 1
            if float(scene_obj[7]) == 100:
                safe_scene += 1
        # 未开始的场景
        if cur_time < start_time:
            safe_scene += 1
        # 当前时间大于场景结束时间，也算未执行的场景
        if cur_time > end_time:
            safe_scene += 1
    # 计算健康度：所有场景加权平均
    if num == 0:
        s_score = 100.00
    else:
        s_score = round(health_degree_total/num,2)
    dic_data["alert_count"] = alert_count;
    dic_data["last_score"] = s_score;
    dic_data["safe_scene"] = safe_scene;
    dic_data["will_scene"] = will_scene;
    dic_data["danger_scene"] = danger_scene;
    return dic_data


def query_alert_data(req):
    """
    告警数据
    :return:
    """
    res = json.loads(req.body)
    alertTime = res.get("alertTime")
    alertLevel = res.get("alertLevel")
    user_dto = user_info.objects.filter(user_name=req.user.username)
    user_vo =user_dto.get()
    pos_list = position_scene.objects.filter(position_id=user_vo.user_pos_id)
    pos_ids = []
    for pos_dto in pos_list:
        pos_ids.append(pos_dto.scene_id)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(alertTime/1000))
    if alertLevel!=None and alertLevel!="-1":
        data = AlertInfo.objects\
            .filter(Q(scene_id__isnull=True) | Q(scene_id__in=pos_ids)) \
            .filter(alert_status_code=alertLevel)\
            .filter(alert_time__gte=time_str)
    else:
        data = AlertInfo.objects\
            .filter(Q(scene_id__isnull=True)|Q(scene_id__in=pos_ids))\
            .filter(alert_time__gte=time_str)
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

    """
    场景类型查询监控
    :param request:
    :return:
    """
    #监控项类型 0 正在执行 1 异常  2 提醒 3未执行
    item_type = request.POST.get("item_type")
    scene_type = request.POST.get("scene_type")

    # 获取用户信息
    user = user_info.objects.get(user_name=request.user.username)
    # 取得用户的岗位
    position_id = model_to_dict(user)['user_pos']
    # 取得岗位下的所有场景
    ps = position_scene.objects.filter(position_id=position_id)
    result = "";
    result+=("(")
    if ps.exists():
        for scene_obj in ps:
            result+=("'")
            result+=(str(model_to_dict(scene_obj)['scene']))
            result+=("'")
            result+=(",")
        result = result[:-1]
        result += (")")
    else:
        result = "('')"

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
            " END FROM "
    if scene_type == "":
        sql_str = sql_str+ " ( SELECT * FROM tb_monitor_scene a WHERE a.id IN "+result+" ) a "\
                           " JOIN tl_scene_monitor b ON a.id = b.scene_id "
    if scene_type != "":
        sql_str = sql_str + " ( SELECT a.* FROM tb_monitor_scene a,"\
            " (SELECT start_time,stop_time FROM system_config_scenetype a "\
            "	WHERE a.scene_type_id = '"+scene_type.decode('utf-8').encode('gb18030') +"' "\
            ") b WHERE a.scene_startTime >= b.start_time "\
            " AND a.scene_endTime <= b.stop_time) a " \
            " JOIN tl_scene_monitor b ON a.id = b.scene_id AND a.id in"+result

    sql_str = sql_str+" JOIN tb_monitor_item c ON b.item_id = c.id " \
            "  JOIN td_gather_data d ON b.item_id = d.item_id "
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


#   张美庆 2019-5-11
#   在界面展示各系统运行情况
def select_All(request):
    result_list = [];  # 存储最后结果，name:场景名,color:颜色
    user = user_info.objects.get(user_name=request.user)
    result = get_every_scene_health_degree(user.id)
    if result.__len__() == 0:
        return tools.success_result(result_list)
    for scene_obj in result:
        my_dict = {}
        cur_time = str(scene_obj[2]);
        start_time = str(scene_obj[3]);
        end_time = str(scene_obj[4]);
        # 正在执行的场景
        if cur_time >= start_time and cur_time <= end_time:
            my_dict["name"] = str(scene_obj[1]) + "(分值：" + str(scene_obj[7]) + ")"
            # 第7个值为场景的得分值
            if float(scene_obj[7]) >= 90 and float(scene_obj[7]) < 100:
                my_dict["color"] = "yellow"
                my_dict["sort"] = "2"
            if float(scene_obj[7]) < 90:
                my_dict["color"] = "red"
                my_dict["sort"] = "1"
            if float(scene_obj[7]) == 100:
                my_dict["color"] = "green"
                my_dict["sort"] = "3"
        # 未开始的场景
        if cur_time < start_time:
            my_dict["name"] = str(scene_obj[1]) + "(未执行)"
            my_dict["color"] = "gray"
            my_dict["sort"] = "4"
        # 当前时间大于场景结束时间，也算未执行的场景
        if cur_time > end_time:
            my_dict["name"] = str(scene_obj[1]) + "(未执行)"
            my_dict["color"] = "gray"
            my_dict["sort"] = "4"
        result_list.append(my_dict)
    result_scene = tools.success_result(result_list)
    return result_scene


def get_every_scene_health_degree(user_id):
    """
    获取当前用户下每一个场景的健康度
    :param user_id:
    :return:
    """
    health_degree_every_scene_sql= "select e.scene_id,d.scene_name,CURRENT_TIME cur_time,d.scene_startTime,d.scene_endTime,e.source_score,e.end_score,e.health_degree " \
                                   +"from (select a.scene_id,a.source_score,IFNULL(b.end_score,0) end_score,round((IFNULL(b.end_score,0)/a.source_score)*100,2) health_degree from "\
                "(select c.scene_id,sum(c.score) source_score from ("\
                " select a.scene_id,b.id,b.score from tb_monitor_item b LEFT JOIN tl_scene_monitor a  on  b.id = a.item_id and a.scene_id in "\
                " (SELECT scene_id FROM tl_position_scene WHERE position_id = ( SELECT user_pos_id FROM tb_user_info WHERE id = "+str(user_id)+")) "\
                " ) c where c.scene_id is not null group by c.scene_id) a LEFT JOIN  "\
                " (select c.scene_id,sum(c.score) end_score from ( "\
                " select a.scene_id,b.item_id,b.score from "\
                " (select DISTINCT a.item_id,IFNULL(a.score,0) score from td_gather_data a,tb_monitor_item b where a.item_id= b.id) b "\
                " LEFT JOIN tl_scene_monitor a  on  b.item_id = a.item_id and a.scene_id in "\
                " (SELECT scene_id FROM tl_position_scene WHERE position_id = ( SELECT user_pos_id FROM tb_user_info WHERE id = "+str(user_id)+")) "\
                " ) c where c.scene_id is not null group by c.scene_id) b "\
                " on a.scene_id = b.scene_id)e LEFT JOIN tb_monitor_scene d ON e.scene_id = d.id "
    db = get_db()
    cursor = db.cursor()
    cursor.execute(health_degree_every_scene_sql)
    res = cursor.fetchall()
    cursor.close()
    return res

