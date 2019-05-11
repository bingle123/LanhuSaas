# -*- coding: utf-8 -*-

import time
import pymysql as MySQLdb
from django.forms import model_to_dict
import shell_app.tools as tools
from conf import settings_development
from history_chart.function import check_jobday
from monitor_scene.models import position_scene
from monitor_item.models import Scene_monitor
from notification.models import TdAlertLog
from position.models import user_info
from datetime import datetime
from models import *
from gather_data.models import TDGatherData


def get_time(request):
    """
    获取当前时间
    :param request:
    :return:
    """
    today = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    flag = check_jobday(1, datetime.now())
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
        last_score = int((all_score - error_score)*100 / all_score)
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
        'alert_data': alert_data,  # 告警table数据
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
