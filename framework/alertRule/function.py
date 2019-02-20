# -*- coding: utf-8 -*-

from models import *
from django.forms.models import model_to_dict
from DataBaseManage.models import *
from DataBaseManage.function import *
import MySQLdb
from gatherData.models import *
from jobManagement.models import Localuser
from system_config.function import *


# 获取所有告警规则
def select_all_rules():
    alert_rules = TbAlertRule.objects.order_by('item_id').all()
    rule_list = []
    for alert_rule in alert_rules:
        create_time = alert_rule.create_time
        edit_time = alert_rule.edit_time
        upper_limit = alert_rule.upper_limit
        lower_limit = alert_rule.lower_limit
        alert_rule.create_time = None
        alert_rule.edit_time = None
        alert_rule.upper_limit = None
        alert_rule.lower_limit = None
        temp = model_to_dict(alert_rule)
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
        rule_list.append(temp)
    return rule_list


# 根据id获取告警规则
def select_rule(rule_data):
    alert_rule = TbAlertRule.objects.filter(id=rule_data['id']).get()
    create_time = alert_rule.create_time
    edit_time = alert_rule.edit_time
    upper_limit = alert_rule.upper_limit
    lower_limit = alert_rule.lower_limit
    alert_rule.create_time = None
    alert_rule.edit_time = None
    alert_rule.upper_limit = None
    alert_rule.lower_limit = None
    selected_rule = model_to_dict(alert_rule)
    if create_time is None:
        selected_rule['create_time'] = ''
    else:
        selected_rule['create_time'] = create_time.strftime('%Y-%m-%d %H:%M:%S')
    if edit_time is None:
        selected_rule['edit_time'] = ''
    else:
        selected_rule['edit_time'] = edit_time.strftime('%Y-%m-%d %H:%M:%S')
    if upper_limit is None:
        selected_rule['upper_limit'] = ''
    else:
        selected_rule['upper_limit'] = str(upper_limit)
    if lower_limit is None:
        selected_rule['lower_limit'] = ''
    else:
        selected_rule['lower_limit'] = str(lower_limit)
    return selected_rule


# 根据ID删除告警规则
def del_rule(rule_data):
    user_count = TlAlertUser.objects.filter(rule_id=rule_data['id']).count()
    if 0 != user_count:
        return "restrict"
    else:
        TbAlertRule.objects.filter(id=rule_data['id']).delete()
        return "ok"


# 根据ID强制删除告警规则
def force_del_rule(rule_data):
    TlAlertUser.objects.filter(rule_id=rule_data['id']).delete()
    TbAlertRule.objects.filter(id=rule_data['id']).delete()
    return "ok"


#告警规则添加
def add_rule(rule_data):
    TbAlertRule(**rule_data).save()
    return "ok"


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