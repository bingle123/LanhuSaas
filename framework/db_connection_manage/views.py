# -*- coding: utf-8 -*-


from common.mymako import render_mako_context


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

