# encoding:utf-8
from function import IqubeInterface
from gather import Gather
from conf.default import MEASURES_API_ADDRESS
from conf.default import LOG_API_ADDRESS
from common.mymako import render_json
import json


# Create your views here.


def get_measures_type(request):
    """
    获得指标类型
    :param request:
    :return:
    """
    res = IqubeInterface.get_api_type(MEASURES_API_ADDRESS)
    return render_json(res)


def get_log_type(request):
    """
    获得日志类型
    :param request:
    :return:
    """
    res = IqubeInterface.get_api_type(LOG_API_ADDRESS)
    return render_json(res)


def gather_base_test(request):
    """

    :param request:
    :return:
    """
    request_body = json.loads(request.body)
    print request_body
    # 维度列表
    dimension_data = request_body['dimension_data']

    # 指标的构造参数
    str = '{hostname=*}'
    for i in dimension_data:
        key = i['dimension_name']
        value = i['dimension_value']
        str += '{' + key + '=' + value + '}'

    interface_type = request_body['interface_type']
    measures = request_body['measures']
    measures_name = request_body['measures_name']
    show_rule_type = request_body['show_rule_type']
    gather_rule = request_body['gather_rule']
    res = Gather.gather_base_test(interface_type=interface_type, measures=measures, measures_name=measures_name,
                                  show_rule_type=show_rule_type, gather_rule=gather_rule, interface_param=str)
    return render_json(res)
    # res = Gather.gather_base_test()
