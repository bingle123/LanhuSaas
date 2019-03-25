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
    interface_type = request_body['interface_type']
    measures = request_body['measures']
    measures_name = request_body['measures_name']
    show_rule_type = request_body['show_rule_type']
    gather_rule = request_body['gather_rule']
    res = Gather.gather_base_test(interface_type=interface_type, measures=measures, measures_name=measures_name,
                                  show_rule_type=show_rule_type, gather_rule=gather_rule)
    return render_json(res)
    # res = Gather.gather_base_test()
