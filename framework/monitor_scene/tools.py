# -*- coding: utf-8 -*-
from django.core.paginator import Paginator
from blueking.component.shortcuts import get_client_by_request


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


def page_paging(abj,limit,page):
    """

    :param abj: 对象
    :param limit: 个数
    :param page: 页数
    :return: 当前页数据，总页数
    """
    p = Paginator (abj, limit)  # 分页
    page_count = p.page_range[-1]  # 总页数
    page_data = p.page(page)  # 当前页数据
    return page_data,page_count


def interface_param(request):
    """
    返回client对象
    :param request:
    :return:
    """
    client = get_client_by_request(request)                         # 获取code、secret参数
    client.set_bk_api_ver('v2')                                     # 以v2版本调用接口
    return client


