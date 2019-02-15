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


# 返回参数gather_status为ok采集正常，返回empty采集结果为空，返回error采集规则错误
def gather_data(info):
    # 临时测试时用的数据，实际应从info对象中获取参数,由celery提供info对象
    # info['id'] = '1'
    # info['gather_params'] = 'sql'
    # info['params'] = '46'
    # info['gather_rule'] = 'SELECT @cp=china_point@,@jp=japan_point@ FROM test_gather_data WHERE id=2'
    # 采集使用的sql
    gather_sql = ''
    # 采集状态，默认为ok
    gather_status = 'ok'
    # 获取数据采集的类型
    gather_type = info['gather_params']
    # 字段索引
    field_start = 7
    field_end = info['gather_rule'].find('FROM') - 1
    # 采集表目标表具体字段
    sql_field = list()
    # 采集表存储的键名
    gather_field = list()
    # 获取采集规则的字段有哪些
    rule_fields_str = info['gather_rule'][field_start:field_end]
    rule_fields = rule_fields_str.split(',')
    for rule_field in rule_fields:
        field = rule_field.strip('@').split('=')
        gather_field.append(field[0])
        sql_field.append(field[1])
    # 生成采集使用的sql
    gather_sql = info['gather_rule'].replace(rule_fields_str, ','.join(sql_field))
    # 采集获取到的key-value
    data_set = []
    for field in gather_field:
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
        #采集规则是否异常判断
        # noinspection PyBroadException
        try:
            cursor.execute(gather_sql)
            result = cursor.fetchall()
        except Exception:
            print 'EXCEPTION'
            gather_status = 'error'
            return gather_status
        # 获取当前采集时间
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if 0 != len(result):
            # 获取当前采集表中的数据是否为空，否则将采集表中的所有数据迁移到历史采集表中
            length = TDGatherData.objects.count()
            # 开始迁移表数据
            if length != 0:
                migrate_data = TDGatherData.objects.all()
                for data in migrate_data:
                    TDGatherHistory(**model_to_dict(data)).save()
                TDGatherData.objects.all().delete()
            # 将结果集整理为key-value形式的采集数据
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
            rule_check()
        else:
            gather_status = 'empty'
    elif "interface" == gather_type:
        pass# 接口方式采集数据待定
    else:
        pass# 文件方式采集数据待定
    return gather_status
