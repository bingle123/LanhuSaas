# -*- coding: utf-8 -*-
import datetime
import re

from guotai.models import *
from common.mymako import render_mako_context, render_json
from blueking.component.shortcuts import get_client_by_request

def home(request):
    """
    国泰君安自动化运维
    """
    return render_mako_context(request, '/guotai/index.html')


def base_index(request):
    """
    国泰君安自动化运维
    """
    return render_mako_context(request, '/guotai/base_index.html')

def test(request):
    client = get_client_by_request(request)
    bk_token = request.COOKIES.get("bk_token")
    bk_biz_list = request.GET.get("bk_biz_list")
    print client
    print bk_token
    print bk_biz_list
    return render_json(
        {
            "bk_token":bk_token,
            "bk_biz_list":bk_biz_list,
            "result": False,
            "code": 1,
            "message": u"未知异常: %s"%('hello'),
            "data": {}
        })