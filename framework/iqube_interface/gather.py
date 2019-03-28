# encoding:utf-8
from conf.default import MEASURES_QUERY_API
from shell_app.tools import success_result
from shell_app.tools import error_result
import requests
import json
import time
from conf.default import MEASURES_API_ADDRESS


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
        :param interface_param: 参数
        :return:
        """
        if interface_type == 'log':
            api_address = MEASURES_QUERY_API
        else:
            api_address = MEASURES_QUERY_API

        # 此处参数传递应给予改善, 时间需要改为当前时间的前一天
        query_form = api_address + '?' + 'start=1551210759&m=sum:sum:' + measures + '_' + measures_name + interface_param

        request_result = requests.get(url=query_form)
        request_code = request_result.status_code
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
                    i['metric_max'] = Gather.percent_manage(gather_rule, i['metric_max'])
                    i['metric_avg'] = Gather.percent_manage(gather_rule, i['metric_avg'])
                # print result_list
                return success_result(temp_list)
            # 显示颜色
            elif show_rule_type == '1':

                # 转换颜色规则
                color_code_map = {}
                rule_list = gather_rule.split('@')
                for i in rule_list:
                    if i is not None:
                        color_rgb = i.split('==')[0]
                        try:
                            color_code = i.split('==')[1]
                        except Exception as e:
                            # 不存在默认将
                            color_code = 'error'
                        color_code_map[color_code] = color_rgb

                # 模拟数据
                temp_list = [{"system_name": "jzjy", "ip": "192.168.1.153", "cpu_cpu_used_pct": 2, "time": "2019-03-22 19:42:12"}, {"system_name": "jzjy", "ip": "192.168.1.157", "cpu_cpu_used_pct": 0, "time": "2019-03-22 19:37:23"}, {"system_name": "jzjy", "ip": "192.168.1.165", "cpu_cpu_used_pct": 0, "time": "2019-03-22 19:41:56"}]

                result_list = Gather.color_manage(color_code_map, temp_list, measures, measures_name)
                return result_list
            # 显示单位
            elif show_rule_type == '2':
                try:
                    for i in temp_list:
                        i[measures + '_' + measures_name] = Gather.other_manage(i[measures + '_' + measures_name], gather_rule)
                    return success_result(temp_list)
                except Exception as e:
                    return error_result(u'异常'+str(e))
        elif request_code == '500':
            return error_result(u'接口请求错误')
        elif request_code == '404':
            return error_result(u'接口找不到了')
        else:
            return error_result(request_code + u'系统错误')

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
            for key, value in i['dps'].items():
                time_list.append(key)
                temp_value = value
                # 最大值
                if value >= temp_value:
                    metric_max = i['dps'][key]
                    metric_max_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(key)))
                # 平均值
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
            map['system_name'] = appsystem
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
    def color_manage(cls, color_code_map, result_list, measures, measures_name):
        """
        颜色管理
        :param color_code_map:               颜色字典
        :param result_list:             change_json方法返回的json,返回的List json
        :param measures:                指标集
        :param measures_name:           指标集名称
        :return:
        """
        try:
            # 颜色代码List
            key_list = []
            for key in color_code_map:
                key_list.append(key)
            for i in result_list:
                color_code = str(i[measures + '_' + measures_name])
                if color_code in key_list:
                    i[measures + '_' + measures_name] = color_code_map[str(i[measures + '_' + measures_name])]
            return success_result(result_list)
        except Exception as e:
            return error_result(u'颜色转换出错'+str(e))

    @classmethod
    def other_manage(cls, original_value, gather_rule):
        """
        其他
        :param original_value:                 原始值
        :param gather_rule:                     规则
        :return:
        """
        rule_list = gather_rule.split('@')
        multiple = rule_list[0]
        unit = rule_list[1]
        return "%.2f" % (float(original_value) * int(multiple)) + unit
