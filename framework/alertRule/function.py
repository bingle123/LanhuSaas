# -*- coding: utf-8 -*-

from models import *
from django.forms.models import model_to_dict
from DataBaseManage.models import *
from DataBaseManage.function import *
import MySQLdb
from gatherData.models import *


def rule_check():
    gather_data = TDGatherData.objects.all()
    for data in gather_data:
        selected_rule = TbAlertRule.objects.filter(item_id=data.item_id, key_name=data.data_key).get()
        print data.data_value
        values = data.data_value.split(',')
        for value in values:
            if float(value) > selected_rule.upper_limit:
                print 'FIELD : %s, ALERT!!!!! VALUE %s TOP OUT OF %s' % (data.data_key, value, selected_rule.upper_limit)
            elif float(value) < selected_rule.lower_limit:
                print 'FIELD : %s, ALERT!!!!! VALUE %s DOWN OUT OF %s' % (data.data_key, value, selected_rule.lower_limit)
    return "ok"
