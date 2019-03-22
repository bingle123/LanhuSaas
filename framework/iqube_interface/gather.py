# encoding:utf-8
from conf.default import MEASURES_QUERY_API
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
    def gather_base_test(cls, interface_type, measures, measures_name, gather_rule, show_rule_type):
        if interface_type == 'log':
            api_address = MEASURES_QUERY_API
        else:
            api_address = MEASURES_QUERY_API

        query_form = api_address + '?' + 'start=1h-ago&m=sum:sum:' + measures + '_' + measures_name + '{hostname=*}'
        result_json = json.loads(requests.get(url=query_form).content)
        # 此处解析结果
        result_list = []
        for i in result_json:
            time_list = []
            for key, value in i['dps'].items():
                time_list.append(key)
            max_time = max(time_list)
            metric = i['dps'][max_time]
            max_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(max_time)))
            map = {}
            map[measures + '_' + measures_name] = metric
            map['time'] = max_time
            appsystem = i['tags']['appsystem']
            ip = i['tags']['ip']
            map['system_name'] = appsystem
            map['ip'] = ip
            result_list.append(map)

        # 此处规则转换
        for i in result_list:
            i['metric'] = Gather.percent_manage(gather_rule, i['metric'])
        print result_list
        return result_list

    @classmethod
    def change_json(cls, measures):
        """

        :param measures:
        :return:
        """
        pass

    @classmethod
    def percent_manage(cls, multiple, original_value):
        """

        :param multiple: 倍数
        :param original_value: 原始值
        :return:
        """
        return "%.2f%%" % (float(original_value) * int(multiple))