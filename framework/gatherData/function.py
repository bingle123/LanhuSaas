# -*- coding: utf-8 -*-

from models import *
from django.forms.models import model_to_dict
from DataBaseManage.models import *
from DataBaseManage.function import *
import MySQLdb
import datetime
import json
import urllib
import urllib2
import os
from gatherData.models import *
from gatherDataHistory.models import *
from alertRule.function import *
from account.models import *
from blueking.component.shortcuts import *


# -------------------- 采集测试规则设定------------------------
# 1. 针对于数据库的数据采集：
# 采集规则的设置类似于SQL语法，但是在字段域有所不同：如@cp=china_point@表示保存在采集表中的字段名称为cp，
# 实际进行目标数据库表采集的字段是china_point
# 2. 针对于接口的数据采集：
# 采集规则为接口执行脚本，返回采集的JSON字符串
# 3. 针对于文件的数据采集：
# 采集规则为linux快速执行脚本，采集数据由脚本保存到采集表gather_data中
# --------------------------------------------------------------


# 采集测试参数初始化方法
def gather_test_init():
    info = dict()
    # ------------临时测试时用的数据，实际应从info对象中获取参数,由celery提供info对象--------
    # sql测试用监控项ID：'1'
    # 接口测试用监控项ID：'2'
    # 文件测试用监控项ID：'3'
    info['id'] = '888'
    # sql测试用类型：'sql'
    # 文件测试用类型：'file'
    # 接口测试用类型：'interface'
    info['gather_params'] = 'interface'
    # sql测试用参数：'46'
    # 文件测试用参数：'192.168.1.10 /fk/test.txt'
    # 接口测试用参数：'http://www.baidu.com,user=root&password=123'
    info['params'] = 'http://t.weather.sojson.com/api/weather/city/,101030100'
    # sql测试用采集规则：'SELECT @cp=china_point@,@jp=japan_point@ FROM test_gather_data WHERE id=2'
    # 文件测试用采集规则：'echo "1234"'
    # 接口测试用采集规则：'接口采集规则'
    info['gather_rule'] = 'url=$1\ncode=$2\nwget http://t.weather.sojson.com/api/weather/city/$code\ncat ./$code'
    # ------------------------------------------------------------------------------------
    return info


# 采集参数解析
def gather_param_parse(info):
    # 采集参数对象
    gather_params = dict()
    # 采集目标具体字段
    gather_params['target_field'] = list()
    # 采集表存储的键名
    gather_params['gather_field'] = list()
    # 采集所需的一些额外参数
    gather_params['extra_param'] = dict()
    if 'sql' == info['gather_params']:
        # 字段索引
        field_start = 7
        field_end = info['gather_rule'].find('FROM')
        if -1 == field_end:
            field_end = info['gather_rule'].find('from')
        # 获取采集规则的字段有哪些
        gather_params['rule_fields_str'] = info['gather_rule'][field_start:field_end].strip(' ')
        # 获取采集域
        rule_fields = gather_params['rule_fields_str'].split(',')
        for rule_field in rule_fields:
            field = rule_field.strip(' ').strip('@').split('=')
            gather_params['gather_field'].append(field[0])
            gather_params['target_field'].append(field[1])
        # 根据参数获取数据库连接配置
        conn_info = Conn.objects.filter(id=info['params']).get()
        # 解密存储在数据库中的数据库密码
        conn_info.password = decrypt_str(conn_info.password)
        gather_params['extra_param']['connection_param'] = conn_info
    elif 'interface' == info['gather_params']:
        interface_params = info['params'].split(',')
        # 获取接口url参数
        interface_url = interface_params[0]
        # 获取调用接口所需的参数
        interface_params = interface_params[1]
        gather_params['extra_param']['interface_url'] = interface_url
        gather_params['extra_param']['script_params'] = interface_url + ' ' + interface_params
        gather_params['gather_rule'] = info['gather_rule']
    elif 'file' == info['gather_params']:
        gather_params['extra_param']['script_params'] = info['params']
        gather_params['gather_rule'] = info['gather_rule']
    elif 'space_interface' == info['gather_params']:
        pass
    return gather_params


# 重复的采集字段数据迁移到历史记录
def gather_data_migrate(item_id):
    # 获取当前采集表中的数据是否为空，否则可能需要将某监控项的采集数据迁移到历史采集表中
    length = TDGatherData.objects.count()
    # 数据采集表存在数据的情况
    if 0 != length:
        # 如果采集表中存在监控项id与当前采集的监控项id对应相同的数据，则将采集表中的此部分数据移至历史记录
        length2 = TDGatherData.objects.filter(item_id=item_id).count()
        if 0 != length2:
            # 开始迁移表数据
            migrate_data = TDGatherData.objects.filter(item_id=item_id).all()
            for data in migrate_data:
                TDGatherHistory(**model_to_dict(data)).save()
            TDGatherData.objects.filter(item_id=item_id).all().delete()


# 数据库采集的key-value定义
def sql_kv_process(gather_field, sql_result):
    data_set = list()
    for field in gather_field:
        temp = dict()
        temp['key'] = field.strip()
        temp['value'] = list()
        temp['value_str'] = ''
        data_set.append(temp)
    # 将结果集整理为key-value形式的采集数据
    for unit in sql_result:
        count = 0
        for data in unit:
            t = data_set[count]
            t['value'].append(str(data))
            t['value_str'] = ','.join(t['value'])
            count += 1
    return data_set


# 接口数据采集的key-value定义
def interface_kv_process(json_dict):
    data_set = list()
    for key, value in json_dict.items():
        temp = dict()
        if isinstance(value, dict):
            temp['value'] = json.dumps(value)
        else:
            temp['value'] = value
        temp['key'] = key
        data_set.append(temp)
    return data_set


# 遍历JSON字典中的所有key：json_dict需要递归的JSON字典，target_field目标采集字段，data_set采集结果，json_path当前遍历的JSON路径
# def recursion_json_dict(json_dict, target_field, data_set, json_path):
#     if isinstance(json_dict, dict):
#         # 遍历，筛选，并将结果集整理为key-value形式的采集数据
#         for key, value in json_dict.items():
#             # 如果当前遍历的还是一个字典，递归遍历该字典
#             if isinstance(value, dict):
#                 # '%s.%s' % (json_path, key)使用.拼接当前key与JSON上层JSON路径，获得当前JSON路径
#                 recursion_json_dict(value, target_field, data_set, '%s.%s' % (json_path, key))
#             # 如果当期遍历的是一个数组，遍历当前数组，然后递归数组中的字典
#             elif isinstance(value, list):
#                 for v in value:
#                     recursion_json_dict(v, target_field, data_set, '%s.%s' % (json_path, key))
#             else:
#                 json_path = '%s.%s' % (json_path, key)
#                 # print "PATH: %s" % json_path
#                 count = 0
#                 for field in target_field:
#                     # 获取需要采集的字段名称single_key
#                     index = field.rfind('.')
#                     if -1 != index:
#                         single_key = field[index + 1:]
#                     else:
#                         single_key = field
#                     # print 'FIELD: %s, SINGLE_KEY: %s, KEY: %s, JSON_PATH: %s' % (field, single_key, key, json_path)
#                     # 判断当前遍历的key是否是需要采集的字段
#                     if single_key == key:
#                         # 判断当前的JSON路径是否符合需要采集的字段的JSON路径
#                         if str(json_path).endswith(field):
#                             # 保存当前JSON节点信息
#                             t = data_set[count]
#                             t['value'].append(str(value))
#                             t['value_str'] = ','.join(t['value'])
#                     count += 1
#                 # print 'PATH: %s' % json_path
#                 # 遍历完当前JSON节点后，回退到上一层节点继续遍历
#                 index1 = json_path.rfind('.')
#                 json_path = json_path[0:index1]


# 采集方法，返回参数gather_status为ok采集正常，返回empty采集结果为空，返回error采集规则错误
def gather_data(info):
    # 采集测试参数初始化
    info = gather_test_init()
    # 获取数据采集的类型
    gather_type = info['gather_params']
    # 采集数据库中的数据
    if "sql" == gather_type:
        # 获取采集参数
        gather_params = gather_param_parse(info)
        # 生成数据库采集使用的sql
        gather_sql = info['gather_rule'].replace(gather_params['rule_fields_str'], ','.join(gather_params['target_field']))
        # 获取数据库连接参数
        conn_params = gather_params['extra_param']['connection_param']
        # 历史采集数据迁移
        gather_data_migrate(info['id'])
        # 连接指定数据库
        try:
            conn = MySQLdb.connect(host=conn_params.ip, user=conn_params.username, passwd=conn_params.password, db=conn_params.databasename, port=int(conn_params.port))
        except Exception as e:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            TDGatherData(item_id=info['id'], gather_time=now, data_key='DB_CONNECTION', data_value='-1',gather_error_log=str(e)).save()
            return "error"
        # 采集规则是否异常判断
        # noinspection PyBroadException
        cursor = conn.cursor()
        cursor.execute('SET NAMES UTF8')
        try:
            cursor.execute(gather_sql)
            result = cursor.fetchall()
        except Exception as e:
            # 保存采集规则错误信息到采集表中
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            TDGatherData(item_id=info['id'], gather_time=now, data_key='DB_CONNECTION', data_value='-2', gather_error_log=str(e)).save()
            return "error"
        # 获取当前采集时间
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if 0 != len(result):
            # 定义key-value
            data_set = sql_kv_process(gather_params['gather_field'], result)
            # 将采集的数据保存到td_gather_data中
            for item in data_set:
                TDGatherData(item_id=info['id'], gather_time=now, data_key=item['key'], data_value=item['value_str']).save()
            return "success"
        else:
            TDGatherData(item_id=info['id'], gather_time=now, data_key='DB_CONNECTION', data_value='0').save()
            return "empty"
    elif "interface" == gather_type:
        # 接口方式采集数据
        # 获取采集参数
        gather_params = gather_param_parse(info)
        # 判断接口连接状态
        if not os.path.exists('./gather_data.sh'):
            f = open('./ping_interface.sh', 'w')
            f.write('echo ping $1 -c 1 -s 1 -W 1 | grep "100% packet loss" | wc -l')
            f.close()
            print './ping_interface.sh' + " created."
        else:
            print './ping_interface.sh' + " already existed."
        ping_status = os.popen('./ping_interface.sh ' + gather_params['extra_param']['interface_url'])
        # 获取当前采集时间
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if '1' == ping_status:
            TDGatherData(item_id=info['id'], gather_time=now, data_key='URL_CONNECTION', data_value='-1', gather_error_log='request interface timeout.').save()
            return "error"
        # 发送请求，从接口获取JSON数据
        if not os.path.exists('./gather_data.sh'):
            f = open('./gather_data.sh', 'w')
            f.write(gather_params['gather_rule'])
            f.close()
            print './gather_data.sh' + " created."
        else:
            os.remove('./gather_data.sh')
            print './gather_data.sh' + " already existed. remove..."
            f = open('./gather_data.sh', 'w')
            f.write(gather_params['gather_rule'])
            f.close()
            print 'new file ./gather_data.sh' + " created."
        json_data = os.popen('./gather_data.sh ' + gather_params['extra_param']['script_params'])
        # JSON模拟接收的数据，测试时使用
        json_data = '{"username":"mary","age":"20","info":[{"tel":"1234566","mobile_phone":"15566757776","email":{"home":"home@qq.com","company":"company@qq.com","capacity":"2000"}}],"money":{"capacity":"50000","type":"RMB"},"address":[{"city":"beijing","code":"1000022"},{"city":"shanghai","code":"2210444"}]}'
        # 将JSON字符串解析为python字典对象，便于筛选并采集数据
        json_dict = json.loads(json_data)
        # 获取当前采集时间
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 判断接口是否返回了空数据
        if 0 != len(json_dict):
            # 历史采集数据迁移
            gather_data_migrate(info['id'])
            # 将结果集整理为key-value形式的采集数据
            # recursion_json_dict(json_dict, gather_params['target_field'], data_set, gather_params['target_root'])
            data_set = interface_kv_process(json_dict)
            # 将采集的数据保存到td_gather_data中
            for item in data_set:
                TDGatherData(item_id=info['id'], gather_time=now, data_key=item['key'], data_value=item['value']).save()
        else:
            TDGatherData(item_id=info['id'], gather_time=now, data_key='URL_CONNECTION', data_value='0').save()
            return 'empty'
    elif "file" == gather_type:
        # 文件方式采集数据
        user_account = BkUser.objects.filter(id=1).get()
        # 根据id为1的用户获取客户端操作快速执行脚本
        client = get_client_by_user(user_account)
        client.set_bk_api_ver('v2')
        # 获取采集参数
        gather_params = gather_param_parse(info)
        # 脚本内容，使用Base64编码
        script_content = base64.b64encode(gather_params['gather_rule'])
        script_params = json.dumps(gather_params['extra_param']['script_params'])
        print 'SCRIPT_PARAMS: %s' % script_params
        # 蓝鲸业务ID，暂固定为2
        biz_id = '2'
        # 蓝鲸云区域ID，暂固定为0
        cloud_id = '0'
        # 蓝鲸Agent所在IP地址，暂固定为192.168.1.52
        agent_id = '192.168.1.52'
        # 向蓝鲸平台请求执行快速执行脚本
        bk_params = {
            'bk_biz_id': biz_id,
            'script_content': script_content,
            'script_param': script_params,
            'is_param_sensitive': 0,
            'account': 'root',
            'script_type': 1,
            'ip_list': [
                {
                    'bk_cloud_id': cloud_id,
                    'ip': agent_id
                }
            ]
        }
        res = client.job.fast_execute_script(bk_params)
        if 'success' != res['message']:
            return 'error'
    # 数据采集完毕后使用告警规则检查数据合法性
    elif "space_interface" == gather_type:
        now = datetime.datetime.now ().strftime ('%Y-%m-%d %H:%M:%S')
        TDGatherData (item_id=info['id'], gather_time=now, data_key=info['message'], data_value=info['message_value'],
                      gather_status='success').save ()
    if None != info['id']:
        rule_check(info['id'])
    return 'success'
