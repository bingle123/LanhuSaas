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
        for value in data.data_value:
            if value > selected_rule.upper_limit or value < selected_rule.lower_limit:
                print 'FIELD : %s, ALERT!!!!!' % data.data_key
                break
    return "ok"
