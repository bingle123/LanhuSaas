# encoding:utf-8
from function import IqubeInterface
from conf.default import MEASURES_API_ADDRESS
from conf.default import LOG_API_ADDRESS
from common.mymako import render_json
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