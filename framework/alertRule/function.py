# -*- coding: utf-8 -*-

from models import *
from django.forms.models import model_to_dict
from DataBaseManage.models import *
from DataBaseManage.function import *
import MySQLdb
from gatherData.models import *
from jobManagement.models import Localuser
from system_config.function import *


def rule_check(monitor_id):
    print 'monitor_id=%s-----Rule checking....' % monitor_id
    # 告警信息
    alert_infos = list()
    # 告警标志位
    alert_flag = False
    # 获取当前监控项下的所有采集数据
    gather_data = TDGatherData.objects.filter(item_id=monitor_id).all()
    for data in gather_data:
        #如果当前采集数据有对应的告警规则
        if 0 != TbAlertRule.objects.filter(item_id=data.item_id, key_name=data.data_key).count():
            selected_rule = TbAlertRule.objects.filter(item_id=data.item_id, key_name=data.data_key).get()
            # 只处理单值情况的告警，多值情况下的采集数据忽略
            if ',' not in data.data_value:
                # 告警规则配置了上限值和下限值的情况
                if selected_rule.upper_limit is not None and selected_rule.lower_limit is not None:
                    if float(data.data_value) > selected_rule.upper_limit or float(data.data_value) < selected_rule.lower_limit:
                        print 'FIELD : %s, ALERT!!!!! VALUE %s OUT OF RANGE' % (data.data_key, data.data_value)
                        alert_flag = True

                # 告警规则仅配置了上限值的情况
                elif selected_rule.upper_limit is not None and selected_rule.lower_limit is None:
                    if float(data.data_value) > selected_rule.upper_limit:
                        print 'FIELD : %s, ALERT!!!!! VALUE %s OUT OF RANGE' % (data.data_key, data.data_value)
                        alert_flag = True
                # 告警规则仅配置了下限值的情况
                elif selected_rule.upper_limit is None and selected_rule.lower_limit is not None:
                    if float(data.data_value) < selected_rule.lower_limit:
                        print 'FIELD : %s, ALERT!!!!! VALUE %s OUT OF RANGE' % (data.data_key, data.data_value)
                        alert_flag = True
                if alert_flag:
                    # 获取当前告警时间
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # 搜集告警信息
                    alert_info = dict()
                    alert_info['rule_id'] = selected_rule.id
                    alert_info['item_id'] = data.item_id
                    alert_info['alert_time'] = now
                    alert_info['alert_title'] = selected_rule.alert_title
                    alert_info['alert_content'] = selected_rule.alert_content
                    alert_info['staff_user'] = list()
                    alert_user_results = TlAlertUser.objects.filter(rule_id=selected_rule.id).all()
                    for alert_user in alert_user_results:
                        alert_info['staff_user'].append(alert_user.user_id)
                    alert_infos.append(alert_info)
            else:
                print 'INFO: Multiple value, rule check skip.......'
    # 如果搜集到了告警信息，将alert_infos对象传递给celery并通知处理告警
    if 0 != len(alert_infos):
        #邮箱被封暂时不能用了 send_alert(**alert_info)
        pass
    return "ok"

def send_alert(**msg):
    alert_title=msg['alert_title']
    alert_content=msg['alert_content']
    staff_users_ids=msg['staff_user']
    msg.update({'persons': msg.pop("staff_user")})
    print msg
    receivers=[]
    for id in staff_users_ids:
        eml=Localuser.objects.get(id=id).email
        receivers.append(eml)
    print receivers
    mail_send(alert_title, alert_content, receivers)
    TdAlertLog.objects.create(**msg)