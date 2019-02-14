# -*- coding: utf-8 -*-

from models import *
from django.forms.models import model_to_dict
from DataBaseManage.models import *
from DataBaseManage.function import *
import MySQLdb
import datetime
from gatherData.models import *
from gatherDataHistory.models import *
from alertRule.function import *


def gather_data(info):
    # 临时测试时用的数据，实际应从info对象中获取参数,由celery提供info对象
    info['id'] = '1'
    info['gather_params'] = 'sql'
    info['params'] = '46'
    info['gather_rule'] = 'SELECT china_point, japan_point FROM test_gather_data'
    # 获取数据采集的类型
    gather_type = info['gather_params']
    # 获取采集规则的字段有哪些
    fields = info['gather_rule'][6:info['gather_rule'].find('FROM')].split(',')
    # 采集获取到的key-value
    data_set = []
    for field in fields:
        temp = dict()
        temp['key'] = field.strip()
        temp['value'] = list()
        temp['value_str'] = ''
        data_set.append(temp)
    # 采集数据库中的数据
    if "sql" == gather_type:
        conn_info = Conn.objects.filter(id=info['params']).get()
        # 解密数据库中的密码
        conn_info.password = decrypt_str(conn_info.password)
        conn = MySQLdb.connect(host=conn_info.ip, user=conn_info.username, passwd=conn_info.password, db=conn_info.databasename, port=int(conn_info.port))
        cursor = conn.cursor()
        # 获取当前采集表中的数据是否为空，否则将采集表中的所有数据迁移到历史采集表中
        length = TDGatherData.objects.count()
        # 开始迁移表数据
        if length != 0:
            migrate_data = TDGatherData.objects.all()
            for data in migrate_data:
                TDGatherHistory(**model_to_dict(data)).save()
            TDGatherData.objects.all().delete()
        cursor.execute(info['gather_rule'])
        result = cursor.fetchall()
        # 获取当前采集时间
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for unit in result:
            count = 0
            for data in unit:
                t = data_set[count]
                t['value'].append(str(data))
                t['value_str'] = ','.join(t['value'])
                count += 1
        # 将采集的数据保存到td_gather_data中
        for item in data_set:
            TDGatherData(item_id=info['id'], gather_time=now, data_key=item['key'], data_value=item['value_str']).save()
        # rule_check()
    elif "interface" == gather_type:
        pass# 接口方式采集数据待定
    else:
        pass# 文件方式采集数据待定
    return "ok"
