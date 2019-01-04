# -*- coding: utf-8 -*-
from component.shortcuts import get_client_by_request
import time
import pytz
import datetime


def error_result(e):
    """
    失败统一JSON
    :param e:   异常
    :return:    json数据
    """
    result = {
        "result": False,
        "message": u"失败 %s" % e,
        "code": 1,
        "results": None
    }
    return result


def success_result(results):
    """
    成功统一JSON
    :param results:
    :return:
    """
    result = {
        "result": True,
        "message": u'成功',
        "code": 0,
        "results": results,
    }
    return result


def page_paging(request, limit):
    """
    分页方法
    :param request:
    :param limit:   页面容量
    :return:        页面起始页码
    """
    click_page_unicode = request.GET.get("clickPage")  # 获取页面页码数
    if click_page_unicode is None or click_page_unicode == "":  # 页码数是否为空，空时赋值为第一页
        click_page = 1
    else:
        click_page = int(click_page_unicode.encode("utf-8"))  # 对页码进行转码
    start_page = (click_page - 1) * limit  # 接口参数:数据起始页码
    return start_page


def interface_param(request):
    """
    返回client对象
    :param request:
    :return:
    """
    client = get_client_by_request(request)  # 获取code、secret参数
    client.set_bk_api_ver('v2')  # 以v2版本调用接口
    return client


# UTCS时间转换为时间戳 2016-07-31T16:00:00Z
def utc_to_local(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%SZ'):
    utc_time_str = "2016-07-31T16:00:00Z"
    utc_time_str = "2019-01-02T06:54:09.000Z"
    local_tz = pytz.timezone('Asia/Shanghai')
    local_format = "%Y-%m-%d %H:%M"
    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    print time.mktime(time.strptime(time_str, local_format))
    return int(time.mktime(time.strptime(time_str, local_format)))