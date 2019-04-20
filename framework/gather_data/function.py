# -*- coding: utf-8 -*-

from models import *
from django.forms.models import model_to_dict
from db_connection.models import *
from db_connection.function import *
import MySQLdb
import datetime
import json
import urllib
import urllib2
import os
import settings
from gather_data.models import *
from gather_data_history.models import *
from notification.function import *
from account.models import *
from blueking.component.shortcuts import *

# -------------------- 采集测试规则设定------------------------
# 1. 针对于数据库的数据采集：
# 采集规则的设置类似于SQL语法，但是在字段域有所不同：如@cp=china_point@表示保存在采集表中的字段名称为cp，
# 实际进行目标数据库表采集的字段是china_point
# 2. 针对于接口的数据采集：
# 采集规则为linux快速执行脚本，返回采集的JSON字符串
# 3. 针对于文件的数据采集：
# 采集规则为linux快速执行脚本，返回采集的JSON字符串
# agent默认路径：/usr/local/gse/agent/bin
# --------------------------------------------------------------


# 全局变量，定义当前采集时间
GATHER_TIME = ''


def gather_test_init():
    """
    # 采集测试参数初始化方法
    :return:
    """
    info = dict()
    # ------------临时测试时用的数据，实际应从info对象中获取参数,由celery提供info对象--------
    # sql测试用监控项ID：'1'
    # 接口测试用监控项ID：'2'
    # 文件测试用监控项ID：'3'
    info['id'] = '233'
    # sql测试用类型：'sql'
    # 文件测试用类型：'file'
    # 接口测试用类型：'interface'
    info['gather_params'] = 'interface'
    # sql测试用参数：'46'
    # 文件测试用参数：'192.168.1.52#./gather_data_test
    # 接口测试用参数：'http://t.weather.sojson.com/api/weather/city/101030100#{"url": "http://t.weather.sojson.com/api/weather/city/", "code": "101030100"}'
    info[
        'params'] = 'http://t.weather.sojson.com/api/weather/city/101030100#{"url": "http://t.weather.sojson.com/api/weather/city/", "code": "101030100"}'
    # sql测试用采集规则：'SELECT @cp=china_point@,@jp=japan_point@ FROM test_gather_data WHERE id=2'
    # 文件测试用采集规则：'cat ${file_path}'
    # 接口测试用采集规则：'dXJsPSQxCmNvZGU9JDIKYHdnZXQgLXFPIGdhdGhlcl9kYXRhX3RlbXAgJHVybCRjb2RlYApjYXQgZ2F0aGVyX2RhdGFfdGVtcAo='
    info['gather_rule'] = 'cat ${file_path}'
    # ------------------------------------------------------------------------------------
    return info


def gather_param_parse(info):
    """
    采集参数解析
    :param info:
    :return:
    """
    # 声明全局变量-采集时间
    global GATHER_TIME
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
            # sql采集规则中，无论大小写都找不到所需的from字段，从而无法定位采集字段的位置，保存采集规则错误日志并立即返回
            if -1 == field_end:
                TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key='DB_CONNECTION', data_value='-2',
                             gather_error_log='gather rule missing \'from\' field').save()
                return None
        # 获取采集规则的字段有哪些，除去空格处理
        gather_params['rule_fields_str'] = info['gather_rule'][field_start:field_end].strip(' ')
        # 获取采集域
        try:
            rule_fields = gather_params['rule_fields_str'].split(',')
            for rule_field in rule_fields:
                field = rule_field.strip(' ').strip('@').split('=')
                gather_params['gather_field'].append(field[0])
                gather_params['target_field'].append(field[1])
        except Exception as e:
            TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key='DB_CONNECTION', data_value='-2',
                         gather_error_log=str(e)).save()
            return None
        # 根据参数获取数据库连接配置\
        print info['params']
        conn_info = Conn.objects.filter(id=info['params']).get()
        # 解密存储在数据库中的数据库密码
        conn_info.password = decrypt_str(conn_info.password)
        gather_params['extra_param']['connection_param'] = conn_info
    elif 'interface' == info['gather_params']:
        # 使用#切割不同输入框传递过来的所有参数
        interface_params = info['params'].split('#')
        # print interface_params
        # 由于接口的参数定义为JSON形式的字符串，若JSON解析失败，则说明填写的JSON有问题，保存错误日志并立即返回
        try:
            json_params = json.loads(interface_params[1])
        except Exception as e:
            TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key='URL_CONNECTION', data_value='-3',
                         gather_error_log=str(e)).save()
            return None
        # 遍历包含参数的JSON对象，根据参数名称替换对应采集规则（脚本中的参数名称）生成执行脚本
        for key, value in json_params.items():
            info['gather_rule'] = info['gather_rule'].replace('${%s}' % key, value)
        # 接口访问的url
        gather_params['extra_param']['url'] = interface_params[0]
        # 采集规则（脚本内容）
        gather_params['gather_rule'] = info['gather_rule']
        print '-------------file execute script--------'
        print gather_params['gather_rule']
        print '----------------------------------------'
    elif 'file' == info['gather_params']:
        # 使用#切割不同输入框传递过来的所有参数
        file_params = info['params'].split('#')
        # 通过切割获取到文件路径
        gather_params['extra_param']['file_path'] = file_params[1]
        # 通过切割获取到服务器地址
        gather_params['extra_param']['file_server'] = file_params[0]
        # 使用填写的文件路径信息替换脚本中的${file_path}变量，生成执行脚本
        gather_params['gather_rule'] = info['gather_rule'].replace('${file_path}',
                                                                   gather_params['extra_param']['file_path'])
        print '-------------file execute script--------'
        print gather_params['gather_rule']
        print '----------------------------------------'
    elif 'space_interface' == info['gather_params']:
        pass
    return gather_params


def gather_data_migrate(item_id):
    """
    重复的采集字段数据迁移到历史记录
    :param item_id:
    :return:
    """
    # 获取当前采集表中的数据是否为空，否则可能需要将某监控项的采集数据迁移到历史采集表中
    gather_data_count = TDGatherData.objects.count()
    # 数据采集表存在数据的情况
    if 0 != gather_data_count:
        # 如果采集表中存在监控项id与当前采集的监控项id对应相同的数据，则将采集表中的此部分数据移至历史记录
        gather_data_count = TDGatherData.objects.filter(item_id=item_id).count()
        if 0 != gather_data_count:
            # 开始迁移表数据
            migrate_data = TDGatherData.objects.filter(item_id=item_id).all()
            for data in migrate_data:
                TDGatherHistory(**model_to_dict(data)).save()
            TDGatherData.objects.filter(item_id=item_id).all().delete()


def sql_kv_process(gather_field, sql_result):
    """
    数据库采集的key-value定义
    :param gather_field:
    :param sql_result:
    :return:
    """
    data_set = list()
    for field in gather_field:
        temp = dict()
        temp['key'] = field.strip()
        temp['value'] = list()
        temp['value_str'] = ''
        data_set.append(temp)
    # 将结果集整理为key-value形式的采集数据
    print sql_result
    print data_set
    for unit in sql_result:
        count = 0
        for data in unit:
            t = data_set[count]
            if not type(data) == unicode:
                t['value'].append(str(data))
            else:
                t['value'].append(data)
            t['value_str'] = ','.join(t['value'])
            count += 1
    return data_set


def fi_kv_process(json_dict):
    """
    接口与接口数据采集的key-value定义
    :param json_dict:
    :return:
    """
    data_set = list()
    for key, value in json_dict.items():
        temp = dict()
        if isinstance(value, dict):
            # json字符串编码为避免生成字符集问题需加上ensure_ascii=False
            temp['value'] = json.dumps(value, ensure_ascii=False)
        else:
            temp['value'] = value
        temp['key'] = key
        data_set.append(temp)
    return data_set


def gather_data(**info):
    """
    采集方法，返回参数gather_status为ok采集正常，返回empty采集结果为空，返回error采集规则错误
    :param info:
    :return:
    """
    # 声明全局变量-采集时间
    global GATHER_TIME
    # 采集测试参数初始化，实际使用时关闭
    # info = gather_test_init()
    # 开始数据采集，确定当前采集时间
    GATHER_TIME = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 获取数据采集的类型
    gather_type = info['gather_params']
    # 历史采集数据迁移
    gather_data_migrate(info['id'])
    # 解析采集参数
    gather_params = gather_param_parse(info)
    # 解析方法执行完毕后返回None说明解析过程中出现了问题，直接返回
    if None is gather_params:
        return "error"

    # 采集数据库中的数据
    if "sql" == gather_type:
        # 生成数据库采集使用的sql
        gather_sql = info['gather_rule'].replace(gather_params['rule_fields_str'],
                                                 ','.join(gather_params['target_field']))
        # 获取数据库连接参数
        conn_params = gather_params['extra_param']['connection_param']
        # 连接指定数据库
        try:
            print 'DB_ID: %s' % conn_params.id
            conn = getAny_db(conn_params.id)
            # conn = MySQ Ldb.connect(host=conn_params.ip, user=conn_params.username, passwd=conn_params.password, db=conn_params.databasename, port=int(conn_params.port))
        except Exception as e:
            TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key='DB_CONNECTION', data_value='-1',
                         gather_error_log=str(e)).save()
            return "error"
        # 保存连接状态为正常
        TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key='DB_CONNECTION', data_value='1').save()
        cursor = conn.cursor()
        cursor.execute('SET NAMES UTF8')
        # 采集规则是否异常判断
        # noinspection PyBroadException
        try:
            cursor.execute(gather_sql)
            result = cursor.fetchall()
        except Exception as e:
            # 保存采集规则错误信息到采集表中
            TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key='DB_CONNECTION', data_value='-2',
                         gather_error_log=str(e)).save()
            return "error"
        # 正确采集到数据
        if 0 != len(result):
            # 定义key-value
            data_set = sql_kv_process(gather_params['gather_field'], result)
            # 将采集的数据保存到td_gather_data中
            # 将采集的数据拼成一个json串，一个监控项在采集表中只有一条记录（与一体化指标兼容）
            gather_dict = "[{"
            for item in data_set:
                if(gather_dict.__len__() > 2):
                    gather_dict += ","+'"'+item['key']+'"'+":"+'"'+item['value_str']+'"'
                else :
                    gather_dict += '"' + item['key'] + '"' + ":" + '"' + item['value_str'] + '"'
            gather_dict += "}]"
            res = TDGatherData.objects.create(item_id=info['id'], gather_time=GATHER_TIME, data_key="measures",
                         data_value=gather_dict)
            return res
        else:
            # 采集是空结果集的情况
            TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key='DB_CONNECTION', data_value='0').save()
            return "empty"
    elif "interface" == gather_type:
        # 接口方式采集数据

        # 接口方式采集数据
        user_account = BkUser.objects.filter(username='admin').get()
        # 根据id为1的admin用户获取客户端操作快速执行脚本
        client = get_client_by_user(user_account)
        client.set_bk_api_ver('v2')
        # 测试开启，加载本地保存的测试接口的脚本，而不从客户端接收指定的脚本
        # info['gather_rule'] = load_script_content('URL_TEST')
        # 生成测试接口状态的脚本，以客户端填写的url替换脚本中的${url}
        ping_script = base64.b64encode(
            load_script_content('URL_CONNECTION').replace('${url}', gather_params['extra_param']['url']))
        # 调用本地的蓝鲸平台快速执行脚本，检测接口状态
        res1 = execute_script(client, ping_script, None, info['id'], 'URL_CONNECTION', settings.GATHER_DATA_HOST)
        # 调用完毕返回None说明脚本执行出现了问题，直接返回
        if None is res1:
            return "error"
        # 调用本地的蓝鲸平台查询作业执行日志获取执行结果
        res2 = get_execute_result(client, res1['data']['job_instance_id'], info['id'], 'URL_CONNECTION')
        # 调用完毕返回None说明脚本执行出现了问题，直接返回
        if None is res2:
            return "error"
        # 判断接口连接状态
        ping_flag = str(res2['data'][0]['step_results'][0]['ip_logs'][0]['log_content'])
        if -1 == int(ping_flag):
            TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key='URL_CONNECTION', data_value='-1',
                         gather_error_log='request interface timeout.').save()
            return "error"
        # 接口连接状态为正常
        TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key='URL_CONNECTION', data_value='1').save()
        # 调用本地的蓝鲸平台快速执行脚本通过脚本从接口获取JSON数据
        res3 = execute_script(client, base64.b64encode(gather_params['gather_rule']), None, info['id'],
                              'URL_CONNECTION', settings.GATHER_DATA_HOST)
        # 调用完毕返回None说明脚本执行出现了问题，直接返回
        if None is res3:
            return "error"
        # 调用本地的蓝鲸平台查询作业执行日志获取执行结果
        res4 = get_execute_result(client, res3['data']['job_instance_id'], info['id'], 'URL_CONNECTION')
        # 调用完毕返回None说明脚本执行出现了问题，直接返回
        if None is res4:
            return "error"
        # 得到采集的JSON数据
        json_data = res4['data'][0]['step_results'][0]['ip_logs'][0]['log_content']
        # 判断接口是否返回了空数据
        if len(json_data) == 0:
            TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key='URL_CONNECTION', data_value='0').save()
            return "empty"
        # 将JSON字符串解析为python字典对象，便于筛选并采集数据
        json_dict = json.loads(json_data)
        # 将结果集整理为key-value形式的采集数据
        data_set = fi_kv_process(json_dict)
        # 将采集的数据保存到td_gather_data中
        for item in data_set:
            TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key=item['key'],
                         data_value=item['value']).save()
    elif "file" == gather_type:
        # 文件方式采集数据
        user_account = BkUser.objects.filter(username='admin').get()
        # 根据id为1的admin用户获取客户端操作快速执行脚本
        client = get_client_by_user(user_account)
        client.set_bk_api_ver('v2')
        # 测试开启，加载本地保存的测试文件的脚本，而不从客户端接收指定的脚本
        # info['gather_rule'] = load_script_content('FILE_TEST')
        # 生成测试文件是否存在的脚本，以客户端填写的文件路径替换脚本中的${file_path}
        file_exist_script = base64.b64encode(
            load_script_content('FILE_EXIST').replace('${file_path}', gather_params['extra_param']['file_path']))
        # 调用客户端指定的蓝鲸平台服务器查找该服务器下的路径下是否存在文件
        res1 = execute_script(client, file_exist_script, None, info['id'], 'FILE_EXIST',
                              gather_params['extra_param']['file_server'])
        # 调用完毕返回None说明脚本执行出现了问题，直接返回
        if None is res1:
            return "error"
        # 调用客户端指定的蓝鲸平台服务器查询作业执行日志获取执行结果
        res2 = get_execute_result(client, res1['data']['job_instance_id'], info['id'], 'FILE_EXIST')
        # 调用完毕返回None说明脚本执行出现了问题，直接返回
        if None is res2:
            return "error"
        # 检测文件是否存在
        file_flag = str(res2['data'][0]['step_results'][0]['ip_logs'][0]['log_content'])
        if -1 == int(file_flag):
            TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key='FILE_EXIST', data_value='-1',
                         gather_error_log='file not exist').save()
            return "error"
        # 文件状态存在
        TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key='FILE_EXIST', data_value='1').save()
        # 调用客户端指定的蓝鲸平台服务器从指定路径下获取文件内容
        res3 = execute_script(client, base64.b64encode(gather_params['gather_rule']), None, info['id'], 'FILE_EXIST',
                              gather_params['extra_param']['file_server'])
        # 调用完毕返回None说明脚本执行出现了问题，直接返回
        if None is res3:
            return "error"
        # 调用客户端指定的蓝鲸平台服务器查询作业执行日志获取执行结果
        res4 = get_execute_result(client, res3['data']['job_instance_id'], info['id'], 'FILE_EXIST')
        # 调用完毕返回None说明脚本执行出现了问题，直接返回
        if None is res4:
            return "error"
        # 得到采集的JSON数据
        json_data = res4['data'][0]['step_results'][0]['ip_logs'][0]['log_content']
        # print json_data
        # 判断采集文件是否返回了空数据
        if len(json_data) == 0:
            TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key='FILE_EXIST', data_value='0').save()
            return "empty"
        json_dict = json.loads(json_data)
        # 将结果集整理为key-value形式的采集数据
        data_set = fi_kv_process(json_dict)
        # 将采集的数据保存到td_gather_data中
        for item in data_set:
            TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key=item['key'],
                         data_value=item['value']).save()
    # 处理监控项空格参数
    elif "space_interface" == gather_type:
        # 结果状态为3的是成功其他为失败
        if info['data_key'] == 3:
            # 存储成功数据
            TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key=info['data_key'],
                         data_value=info['data_value'],
                         gather_error_log=None, instance_id=info['instance_id']).save()
        else:
            # 存储失败数据及日志
            TDGatherData(item_id=info['id'], gather_time=GATHER_TIME, data_key=info['data_key'],
                         data_value=info['data_value'],
                         gather_error_log=info['gather_error_log'], instance_id=info['instance_id']).save()
    # 数据采集完毕后使用告警规则检查数据合法性
    if None != info['id']:
        rule_check(info['id'])

    return 'success'


def execute_script(client, script_content, script_params, item_id, execute_type, execute_server):
    """

    :param client:
    :param script_content:
    :param script_params:
    :param item_id:
    :param execute_type:
    :param execute_server:
    :return:
    """
    # 声明全局变量-采集时间
    global GATHER_TIME
    # 蓝鲸业务ID，暂固定为2
    biz_id = '2'
    # 蓝鲸云区域ID，暂固定为0
    cloud_id = '0'
    # 蓝鲸Agent所在IP地址
    agent_id = execute_server
    # 向蓝鲸平台请求执行快速执行脚本
    script_bk_params = {
        'bk_biz_id': biz_id,
        'script_content': script_content,
        'script_param': script_params,
        'account': 'root',
        'ip_list': [
            {
                'bk_cloud_id': cloud_id,
                'ip': agent_id
            }
        ]
    }
    res = client.job.fast_execute_script(script_bk_params)
    # 脚本执行出错
    if '0' != str(res['code']):
        TDGatherData(item_id=item_id, gather_time=GATHER_TIME, data_key=execute_type, data_value='-2',
                     gather_error_log=str(res['message'])).save()
        return None
    return res


def get_execute_result(client, job_instance_id, item_id, execute_type):
    """

    :param client:
    :param job_instance_id:
    :param item_id:
    :param execute_type:
    :return:
    """
    # 声明全局变量-采集时间
    global GATHER_TIME
    # 向蓝鲸平台请求执行作业平台日志
    job_log_bk_params = {
        'bk_biz_id': 2,
        'job_instance_id': job_instance_id
    }
    res = client.job.get_job_instance_log(job_log_bk_params)
    # 脚本执行出错
    if 0 != int(res['code']):
        TDGatherData(item_id=item_id, gather_time=GATHER_TIME, data_key=execute_type, data_value='-2',
                     gather_error_log=str(res['message'])).save()
        return None
    # 每隔一秒查询一次脚本是否执行完成，执行完成则获取其执行结果
    while 'True' != str(res['data'][0]['is_finished']):
        time.sleep(1)
        res = client.job.get_job_instance_log(job_log_bk_params)
    # print res
    # 脚本执行出错
    if 3 != int(res['data'][0]['status']):
        TDGatherData(item_id=item_id, gather_time=GATHER_TIME, data_key=execute_type, data_value='-2',
                     gather_error_log='script execution failed ').save()
        return None
    return res


def load_script_content(script_type):
    """
    加载本地保存的脚本文件用于测试、检查文件是否存在、接口的连通性
    :param script_type:
    :return:
    """
    if 'FILE_EXIST' == script_type:
        script_path = './static/script/file_exist.sh'
    elif 'URL_CONNECTION' == script_type:
        script_path = './static/script/interface_ping.sh'
    elif 'FILE_TEST' == script_type:
        script_path = './static/script/file_gather_data.sh'
    elif 'URL_TEST' == script_type:
        script_path = './static/script/interface_gather_data.sh'
    script_content = ''
    with open(script_path) as f:
        line = f.readline()
        while line:
            script_content = script_content + line
            line = f.readline()
    return script_content


# 采集数据的保存方法
def gather_data_save(info):
    # 这里要将info['measures']json转为字符类型，监控项采集数据必须是字符个数，才能保证场景编排展示正常
    if 'add' == info['type']:
        TDGatherData.objects.create(item_id=info['item_id'], data_key='measures', data_value=json.dumps(info['measures']))
    elif 'edit' == info['type']:
        TDGatherData.objects.filter(item_id=info['item_id']).update(data_key='measures', data_value=json.dumps(info['measures']))
    else:
        return "error"
    return 'ok'
