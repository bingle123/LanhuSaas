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
from account.models import *
from blueking.component.shortcuts import *


# 返回参数gather_status为ok采集正常，返回empty采集结果为空，返回error采集规则错误
def gather_data(info):
    # 临时测试时用的数据，实际应从info对象中获取参数,由celery提供info对象
    info['id'] = '2'
    # sql测试用类型：sql
    # 文件测试用类型：'file'
    info['gather_params'] = 'file'
    # sql测试用参数：'46'
    # 文件测试用参数：'192.168.1.10,/fk/test.txt'
    info['params'] = '192.168.1.10,/fk/test.txt'
    # sql测试用采集规则：'SELECT @cp=china_point@,@jp=japan_point@ FROM test_gather_data'
    # 文件测试用采集规则：'echo "1234"'
    info['gather_rule'] = 'echo "1234"'
    # 采集状态，默认为ok
    gather_status = 'ok'
    # 获取数据采集的类型
    gather_type = info['gather_params']
    # 采集数据库中的数据
    if "sql" == gather_type:
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
        # 根据参数获取数据库连接配置
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
        # 获取当前采集表中的数据是否为空，否则可能需要将某监控项的采集数据迁移到历史采集表中
        length = TDGatherData.objects.count()
        if 0 != len(result):
            # 采集获取到的key-value
            data_set = list()
            for field in gather_field:
                temp = dict()
                temp['key'] = field.strip()
                temp['value'] = list()
                temp['value_str'] = ''
                data_set.append(temp)
                # 数据采集表存在数据的情况
                if length != 0:
                    # 如果采集表中存在监控项id与当前采集的监控项id对应相同的数据，则将采集表中的此部分数据移至历史记录
                    length2 = TDGatherData.objects.filter(item_id=info['id']).count()
                    if 0 != length2:
                        # 开始迁移表数据
                        migrate_data = TDGatherData.objects.filter(item_id=info['id']).all()
                        for data in migrate_data:
                            TDGatherHistory(**model_to_dict(data)).save()
                        TDGatherData.objects.filter(item_id=info['id']).all().delete()
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
        else:
            gather_status = 'empty'
    elif "interface" == gather_type:
        # 接口方式采集数据
        pass
    else:
        # 文件方式采集数据
        user_account = BkUser.objects.filter(id=4).get()
        # 根据id为1的用户获取客户端操作快速执行脚本
        client = get_client_by_user(user_account)
        client.set_bk_api_ver('v2')
        # 脚本内容，使用Base64编码
        script_content = base64.b64encode(info['gather_rule'])
        temp_param = info['params'].split(',')
        # 目标文件的IP地址
        ip_location = temp_param[0]
        # 目标文件所在服务器的路径
        file_path = temp_param[1]
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
        print res
        # 数据采集完毕后使用告警规则检查数据合法性
        rule_check(info['id'])
    return gather_status
