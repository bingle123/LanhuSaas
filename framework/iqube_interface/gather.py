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
    def gather_base_test(cls, interface_type, measures, measures_name, gather_rule, show_rule_type):
        """
        基本单元采集测试
        :param interface_type: 接口类型 log为日志,measures为指标类型
        :param measures:        指标集
        :param measures_name:   指标名称
        :param gather_rule:     解析规则
        :param show_rule_type:  显示类型 0/百分比, 1/颜色, 2/不变化
        :return:
        """
        if interface_type == 'log':
            api_address = MEASURES_QUERY_API
        else:
            api_address = MEASURES_QUERY_API

        query_form = api_address + '?' + 'start=1551210759&m=sum:sum:' + measures + '_' + measures_name + '{hostname=*}'
        request_result = requests.get(url=query_form)
        request_code = request_result.status_code
        if request_code == 200:
            # 百分比
            if show_rule_type == '0':
                # API请求结果
                result_json = json.loads(request_result.content)
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
                    i[measures + '_' + measures_name] = Gather.percent_manage(gather_rule, i[measures + '_' + measures_name])
                # print result_list
                return success_result(result_list)
            # 显示颜色
            elif show_rule_type == '1':
                pass

            # 显示单位
            elif show_rule_type == '2':
                pass
        elif request_code == '500':
            return error_result(u'接口请求错误')
        elif request_code == '404':
            return error_result(u'接口找不到了')
        else:
            return error_result(request_code + u'系统错误')

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