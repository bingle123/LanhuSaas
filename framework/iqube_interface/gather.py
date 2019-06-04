# encoding:utf-8
from conf.default import MEASURES_QUERY_API
from shell_app.tools import success_result
from shell_app.tools import error_result
from gather_data.models import TDGatherData
import requests
import json
import time
import sys
from conf.default import MEASURES_API_ADDRESS
from db_connection.function import get_db

# 解决ascii编码的问题
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class Gather():
    """
    采集类
    """

    def __init__(self):
        pass

    @classmethod
    def gather_base_test(cls, interface_type, measures, measures_name, gather_rule, show_rule_type, interface_param):
        """
        基本单元采集测试
        :param interface_type: 接口类型 log为日志,measures为指标类型
        :param measures:        指标集
        :param measures_name:   指标名称
        :param gather_rule:     解析规则
        :param show_rule_type:  显示类型 0/百分比, 1/颜色, 2/不变化 增加显示类型时请增加注释
        :param interface_param: url参数
        :return:
        """
        # 日志数据模拟
        if interface_type == 'log':
            api_address = MEASURES_QUERY_API
            # 模拟数据
            temp_list = [{"zy-shangpin-initial_system-init": "1"}]
            # 加入颜色展示规则
            for temp in temp_list:
                temp[measures + '_' + measures_name] = Gather.color_manage(temp[measures + '_' + measures_name], gather_rule)
            # 返回统一出来的结果
            return success_result(temp_list)
        else:
            api_address = MEASURES_QUERY_API
        # 获取当前系统时间前10秒的时间戳
        result = get_previous_second_ts()
        curr_ts = str(list(result[0])[0])
        # 此处参数传递应给予改善, 时间需要改为当前时间的前一天
        query_form = api_address + '?' + 'start='+curr_ts+'&m=sum:sum:' + measures + '_' + measures_name + interface_param
        timeout_result = get_icube_timeout()
        icube_timeout = int(list(timeout_result[0])[0])
        # 设置调用服务的超时时长在数据库中配置，超过配置的时长就抛异常
        request_result = requests.get(url=query_form,timeout=icube_timeout)
        request_code = request_result.status_code
        print request_result
        if request_code == 200:
            temp_list = Gather.change_json(measures, request_result, measures_name)
            # 百分比
            if show_rule_type == '0':

                # # API请求结果
                # result_json = json.loads(request_result.content)
                # # 此处解析结果
                # result_list = []
                # for i in result_json:
                #     time_list = []
                #     for key, value in i['dps'].items():
                #         time_list.append(key)
                #     max_time = max(time_list)
                #     metric = i['dps'][max_time]
                #     max_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(max_time)))
                #     map = {}
                #     map[measures + '_' + measures_name] = metric
                #     map['time'] = max_time
                #     appsystem = i['tags']['appsystem']
                #     ip = i['tags']['ip']
                #     map['system_name'] = appsystem
                #     map['ip'] = ip
                #     result_list.append(map)

                # 此处规则转换
                for i in temp_list:
                    i[measures + '_' + measures_name] = Gather.percent_manage(gather_rule, i[measures + '_' + measures_name])
                    # i['metric_max'] = Gather.percent_manage(gather_rule, i['metric_max'])
                    # i['metric_avg'] = Gather.percent_manage(gather_rule, i['metric_avg'])
                # print result_list
                return success_result(temp_list)
            # 显示颜色
            elif show_rule_type == '1':

                # 转换颜色规则
                # color_code_map = {}
                # rule_list = gather_rule.split('@')
                # for i in rule_list:
                #     if i is not None:
                #         color_rgb = i.split('==')[0]
                #         try:
                #             color_code = i.split('==')[1]
                #         except Exception as e:
                #             # 不存在默认将
                #             color_code = 'error'
                #         color_code_map[color_code] = color_rgb

                # 模拟数据
                # temp_list = [{"system_name": "jzjy", "ip": "192.168.1.153", "cpu_cpu_used_pct": 2, "time": "2019-03-22 19:42:12"}, {"system_name": "jzjy", "ip": "192.168.1.157", "cpu_cpu_used_pct": 0, "time": "2019-03-22 19:37:23"}, {"system_name": "jzjy", "ip": "192.168.1.165", "cpu_cpu_used_pct": 0, "time": "2019-03-22 19:41:56"}]
                # result_list = Gather.color_manage(color_code_map, temp_list, measures, measures_name)
                try:
                    for i in temp_list:
                        i[measures + '_' + measures_name] = Gather.color_manage(i[measures + '_' + measures_name], gather_rule)
                        # i['metric_max'] = Gather.color_manage(i['metric_max'], gather_rule)
                        # i['metric_avg'] = Gather.color_manage(i['metric_avg'], gather_rule)
                    return success_result(temp_list)
                except Exception as e:
                    print e
                    return error_result(u'异常'+str(e))
            # 其它展示
            elif show_rule_type == '2':
                try:
                    for i in temp_list:
                        i[measures + '_' + measures_name] = Gather.other_manage(i[measures + '_' + measures_name], gather_rule)
                        # i['metric_max'] = Gather.other_manage(i['metric_max'], gather_rule)
                        # i['metric_avg'] = Gather.other_manage(i['metric_avg'], gather_rule)
                    print temp_list
                    return success_result(temp_list)
                except Exception as e:
                    print e
                    return error_result(u'异常'+str(e))
        elif request_code == '500':
            return error_result(u'接口请求错误')
        elif request_code == '404':
            return error_result(u'接口找不到了')
        else:
            return error_result(request_code.__str__() + u'系统错误')

    @classmethod
    def change_json(cls, measures, request_result, measures_name):
        """
        将API结果处理成最新json结果
        :param measures:            指标集
        :param request_result:      API请求结果
        :param measures_name:       指标名称
        :return:
        """
        result_json = json.loads(request_result.content)

        # 此处解析结果
        result_list = []
        for i in result_json:
            # 时间列表
            time_list = []
            # 临时变量
            temp_value = None

            sum_value = 0
            value_count = 0
            metric_max = 0
            for key, value in i['dps'].items():
                time_list.append(key)
                # 最大值
                if value > metric_max:
                    metric_max = i['dps'][key]
                    metric_max_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(key)))
                # 值之和
                sum_value += value
                # 循环次数，用于计算平均值使用
                value_count += 1
            max_time = max(time_list)
            metric = i['dps'][max_time]
            metric_avg = sum_value / value_count
            max_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(max_time)))
            map = {}
            map[measures + '_' + measures_name] = metric
            map['time'] = max_time
            appsystem = i['tags']['appsystem']
            ip = i['tags']['ip']
            map['appsystem'] = appsystem
            map['ip'] = ip

            map['metric_max'] = metric_max
            map['metric_max_time'] = metric_max_time
            map['metric_avg'] = metric_avg

            result_list.append(map)
        return result_list

    @classmethod
    def percent_manage(cls, multiple, original_value):
        """
        百分比管理
        :param multiple: 倍数
        :param original_value: 原始值
        :return:
        """
        return "%.2f%%" % (float(original_value) * int(multiple))

    @classmethod
    def color_manage(cls, original_value, rule_list):
        """
        颜色管理

        :return:
        """
        # 前后台色标是不是一致不重要了
        # 根据前台取色设置的变化，后台规则做的修改
        unit_list = ['#40C7A1', '#FF6161', '#FCB02D', '#B6B6B6', '#FFFFFF']
        temp_color_list = []
        temp_rule_list = []
        # 根据前台传过来的色标共五个，不够用白色填充（前台最多传4个过来）
        processed_rule_list = rule_list.strip().split('\n')
        for color_obj in processed_rule_list:
            temp_rule_list.append(color_obj.split("##")[0])
            temp_color_list.append("#"+color_obj.split("##")[1])
            # 只传了一个值过来
        if len(temp_color_list) == 1:
            unit_list[0] = temp_color_list[0]
            unit_list[1] = "#FFFFFF"
            unit_list[2] = "#FFFFFF"
            unit_list[3] = "#FFFFFF"
            unit_list[4] = "#FFFFFF"
        if len(temp_color_list) == 2:
            unit_list[0] = temp_color_list[0]
            unit_list[1] = temp_color_list[1]
            unit_list[2] = "#FFFFFF"
            unit_list[3] = "#FFFFFF"
            unit_list[4] = "#FFFFFF"
        if len(temp_color_list) == 3:
            unit_list[0] = temp_color_list[0]
            unit_list[1] = temp_color_list[1]
            unit_list[2] = temp_color_list[2]
            unit_list[3] = "#FFFFFF"
            unit_list[4] = "#FFFFFF"
        if len(temp_color_list) == 4:
            unit_list[0] = temp_color_list[0]
            unit_list[1] = temp_color_list[1]
            unit_list[2] = temp_color_list[2]
            unit_list[3] = temp_color_list[3]
            unit_list[4] = "#FFFFFF"
        processed_val = Gather.value_range_process(temp_rule_list, original_value, unit_list)
        return processed_val

    @classmethod
    def other_manage(cls, original_value, gather_rule):
        """
        其他
        :param original_value:                 原始值
        :param gather_rule:                     规则
        :return:
        """
        unit_list = []
        rule_list = gather_rule.split('\n')
        processed_rule_list = list()
        for r_list in rule_list:
            temp_list = r_list.strip().split('@')
            processed_rule_list.append(temp_list[0])
            unit_list.append('@' + temp_list[1])
        # 不足长度为5的用@符号填充
        if len(rule_list) == 1:
            unit_list[0] = unit_list[0]
            unit_list.append("@")
            unit_list.append("@")
            unit_list.append("@")
            unit_list.append("@")
        if len(rule_list) == 2:
            unit_list[0] = unit_list[0]
            unit_list[1] = unit_list[1]
            unit_list.append("@")
            unit_list.append("@")
            unit_list.append("@")
        if len(rule_list) == 3:
            unit_list[0] = unit_list[0]
            unit_list[1] = unit_list[1]
            unit_list[2] = unit_list[2]
            unit_list.append("@")
            unit_list.append("@")
        if len(rule_list) == 4:
            unit_list[0] = unit_list[0]
            unit_list[1] = unit_list[1]
            unit_list[2] = unit_list[2]
            unit_list[3] = unit_list[3]
            unit_list.append("@")
        processed_val = Gather.value_range_process(processed_rule_list, original_value, unit_list)
        return processed_val
        # for item in rule_list:
        #     params = item.split('@')
        #
        #
        # multiple = rule_list[0]
        # unit = rule_list[1]
        # return "%.2f" % (float(original_value) * int(multiple)) + unit

    # 针对不同数值范围添加后缀
    @classmethod
    def value_range_process(cls, rule_list, original_value, unit_list):
        """
        :param rule_list:                 校验规则
        :param original_value:            原始值
        :param unit_list:                 单位数组
        :return:
        """
        if rule_list.__len__() >= 1 and float(rule_list[0].strip().split('-')[0]) <= float(original_value) < float(
                rule_list[0].strip().split('-')[1]):
            return str(original_value) + unit_list[0].__str__()
        elif rule_list.__len__() >= 2 and float(rule_list[1].strip().split('-')[0]) <= float(original_value) < float(
                rule_list[1].strip().split('-')[1]):
            return str(original_value) + unit_list[1].__str__()
        elif rule_list.__len__() >= 3 and float(rule_list[2].strip().split('-')[0]) <= float(original_value) < float(
                rule_list[2].strip().split('-')[1]):
            return str(original_value) + unit_list[2].__str__()
        elif rule_list.__len__() >= 4 and float(rule_list[3].strip().split('-')[0]) <= float(original_value) < float(
                rule_list[3].strip().split('-')[1]):
            return str(original_value) + unit_list[3].__str__()
        else:
            return str(original_value) + unit_list[4].__str__()


def get_previous_second_ts():
    """
        获取当前系统时间前1000秒的时间戳（具体时长在td_scene_design表配置，默认为1000）
        :return:
        """
    res = ""
    try:
        sql = "SELECT unix_timestamp(date_sub(now(), INTERVAL ifnull((SELECT time_interval FROM td_scene_design WHERE task_code = 'index_advance_duration'),1000) SECOND)) as timestamp;"
        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        db.close()
    except Exception as e:
        return tools.error_result(e)
    # scene_list = list(res1)
    return res


def get_icube_timeout():
    """
    调用icube服务超时时长设置
    :return:
    """
    res = ""
    try:
        sql = "select IFNULL(time_interval,5) time_interval from td_scene_design where task_code = 'icube_timeout'"
        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        db.close()
    except Exception as e:
        return tools.error_result(e)
    return res