# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt

from common.mymako import render_mako_context
from common.mymako import render_json
from django.middleware.csrf import get_token
import json


def index(request):
    """
    首页
    """
    return render_mako_context(request, '/db_connection_manage/index.html')


def element(request):
    """
    element页面测试
    :param reuqest:
    :return:
    """
    return render_mako_context(request, '/db_connection_manage/element.html')


def vue_test(request):
    """
    vue 表单新增测试
    :param request:
    :return:
    """
    return render_mako_context(request, '/db_connection_manage/vue_test_add.html')


# @csrf_exempt
def vue_add(request):
    """
    vue 获取json
    :param request:
    :return:
    """
    print get_token(request)
    test = request.body
    print test
    # print request.GET.get("params")
    # print request.method
    # print request.COOKIES.get('csrftoken')
    # print request.COOKIES.get('csrftoken')
    # print request.META["CSRF_COOKIE_USED"]
    return render_json(test)
