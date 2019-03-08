# -*- coding: utf-8 -*-
from django.shortcuts import render
from common.mymako import render_json
from common.mymako import render_mako_context
from . import function
import json
import sys


def show_index(request):
    return render_mako_context(request, './customQuery/customQuery.html')


def select_queries_pagination(request):
    page_info = json.loads(request.body)
    selected_queries = function.select_queries_pagination(page_info)
    return render_json(selected_queries)


def del_query(request):
    query_id = json.loads(request.body)
    status = function.del_query(query_id)
    return render_json(status)


def select_query(request):
    query_id = json.loads(request.body)
    selected_query = function.select_query(query_id)
    return render_json(selected_query)


def add_query(request):
    query_data = json.loads(request.body)
    status = function.add_query(query_data)
    return render_json(status)


def load_all_tables_name(request):
    db = json.loads(request.body)
    status = function.load_all_tables_name(db)
    return render_json(status)


def load_all_fields_name(request):
    tb = json.loads(request.body)
    status = function.load_all_fields_name(tb)
    return render_json(status)