# -*- coding: utf-8 -*-

from models import *
from django.forms.models import model_to_dict
from DataBaseManage.models import *
from DataBaseManage.function import *
import MySQLdb
from gatherData.models import *


def rule_check():
    #获取当前所有的采集数据
    gather_data = TDGatherData.objects.all()
    for data in gather_data:
        selected_rule = TbAlertRule.objects.filter(item_id=data.item_id, key_name=data.data_key).get()
        # 只处理单值情况的告警，多值情况下的采集数据忽略
        if ',' not in data.data_value:
            # 告警规则配置了上限值和下限值的情况
            if selected_rule.upper_limit is not None and selected_rule.lower_limit is not None:
                if float(data.data_value) > selected_rule.upper_limit or float(data.data_value) < selected_rule.lower_limit:
                    print 'FIELD : %s, ALERT!!!!! VALUE %s OUT OF RANGE' % (data.data_key, data.data_value)
            # 告警规则仅配置了上限值的情况
            elif selected_rule.upper_limit is not None and selected_rule.lower_limit is None:
                if float(data.data_value) > selected_rule.upper_limit:
                    print 'FIELD : %s, ALERT!!!!! VALUE %s OUT OF RANGE' % (data.data_key, data.data_value)
            # 告警规则仅配置了下限值的情况
            elif selected_rule.upper_limit is None and selected_rule.lower_limit is not None:
                if float(data.data_value) < selected_rule.lower_limit:
                    print 'FIELD : %s, ALERT!!!!! VALUE %s OUT OF RANGE' % (data.data_key, data.data_value)
    return "ok"
