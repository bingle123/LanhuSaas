# -*- coding: utf-8 -*-

import time
from decimal import Decimal

import MySQLdb
from django.db.models import Q
from django.forms import model_to_dict

import tools
from conf import settings_development
from gather_data_history.models import TDGatherHistory
from history_chart.function import check_jobday, json
from market_day.models import Holiday
from monitor_scene.models import position_scene
from monitor_item.models import Scene_monitor
from notification.models import TdAlertLog
from position.models import user_info
from datetime import datetime

#获取当前时间
def get_time(request):
    today = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    flag = check_jobday(1,datetime.now())
    if flag==True:
        today_name = '交易日'
    elif flag ==False:
        today_name = '非交易日'
    else:
        today_name = None
    dic_data = {
        'time_date':today,
        'today_name':today_name,
    }
    return dic_data

#获取当前用户所对应的岗位下的所有场景监控项的告警
def scenes_alert(request):
    #admin的场景对应94没数据 除数是0会报错
    user = user_info.objects.get(user_name='yanchunlei')
    position_id = model_to_dict(user)['user_pos']
    #一个职位下得所有场景
    ps = position_scene.objects.filter(position_id = position_id)

    alert_log = []
    alert_count = 0
    alert_data = []
    all_avg = 0
    #分别是安全。预警。危险
    safe_scene = 0
    will_scene = 0
    danger_scene = 0
    for i in ps:
        sid = model_to_dict(i)['scene']
        #场景和监控项关联表
        sm = Scene_monitor.objects.filter(scene_id=sid)
        for x in sm:
            all_score = 100
            id = model_to_dict(i)['scene']
            id = str(id)
            #计算一个场景下的总分nums
            try:
                sql = "SELECT sum(score) from tl_scene_monitor where scene_id = '"+id+"' "
                DATABASES = settings_development.DATABASES['default']
                db = MySQLdb.connect(host=DATABASES['HOST'], user=DATABASES['USER'], passwd=DATABASES['PASSWORD'],
                                     db=DATABASES['NAME'], charset="utf8")
                cursor = db.cursor()
                cursor.execute(sql)
                res1 = cursor.fetchall()
                nums = list(res1)
                nums = nums[0][0]
                #如果总分为0,直接为0
                thistory = TDGatherHistory.objects.filter(item_id=model_to_dict(x)['item_id'])
                for hi in thistory:
                    his = model_to_dict(hi)
                    his['gather_time'] = hi.gather_time
                    if str(his['gather_time']).split(' ')[0] == time.strftime("%Y-%m-%d", time.localtime(time.time())):
                        # 如果当天时间此监控项出错，那么就减去此监控项得权值,如果总分为0那all_score直接为0
                        if his['gather_error_log'] != None and his['gather_error_log'] != '':
                            if nums == 0:
                                all_score = 0
                            else:
                                all_score = all_score - model_to_dict(x)['score'] / nums[0]
                        else:
                            pass
            except Exception as e:
                return tools.error_result(e)
            if all_score == 100:
                safe_scene = safe_scene+1
            elif all_score <100 and all_score>90:
                will_scene = will_scene+1
            else:
                danger_scene = danger_scene +1
            all_avg = all_avg + all_score

    #所有场景下得监控项得到的权值分总和/场景数 = 权值平均分 就是从健康度
        last_score = all_avg / ps.__len__()

        alert_log = TdAlertLog.objects.filter(item_id=model_to_dict(x)['item_id'])
        for y in alert_log:
            alertd = model_to_dict(y)
            alertd['alert_time'] = y.alert_time
            if str(alertd['alert_time']).split(' ')[0] == time.strftime("%Y-%m-%d", time.localtime(time.time())):
                alert_count = alert_count + 1
                alertd['alert_time'] = str(alertd['alert_time'])
                alert_data.append(alertd)
        dic_data= {
            'alert_count':alert_count, #告警数
            'alert_data':alert_data,    #告警table数据
            'last_score':last_score,    #健康度
            'safe_scene':safe_scene,
            'will_scene':will_scene,
            'danger_scene':danger_scene,
        }
    return dic_data







