# -*- coding: utf-8 -*-
from common.mymako import render_json
from common.mymako import render_mako_context
from . import function
import json


def show_index(request):
    """

    :param request:
    :return:
    """
    return render_mako_context(request, './custom_query/custom_query.html')


def select_queries_pagination(request):
    """

    :param request:
    :return:
    """
    page_info = json.loads(request.body)
    selected_queries = function.select_queries_pagination(page_info)
    return render_json(selected_queries)


def del_query(request):
    """

    :param request:
    :return:
    """
    query_id = json.loads(request.body)
    status = function.del_query(query_id)
    return render_json(status)


def select_query(request):
    """

    :param request:
    :return:
    """
    query_id = json.loads(request.body)
    selected_query = function.select_query(query_id)
    return render_json(selected_query)


def add_query(request):
    """

    :param request:
    :return:
    """
    query_data = json.loads(request.body)
    status = function.add_query(query_data)
    return render_json(status)


def load_all_tables_name(request):
    """

    :param request:
    :return:
    """
    db = json.loads(request.body)
    status = function.load_all_tables_name(db)
    return render_json(status)


def load_all_fields_name(request):
    """

    :param request:
    :return:
    """
    tb = json.loads(request.body)
    status = function.load_all_fields_name(tb)
    return render_json(status)


def sql_test(req):
    """

    :param req:
    :return:
    """
    sql = json.loads(req.body)
    res = function.sql_test(sql)
    return render_json(res)
