# encoding:utf-8
# encoding:utf-8
import function
import tools
from common.mymako import render_json, render_mako_context
import json

def index(request):
    return render_mako_context(request, './history_chart/history.html')

def show_all(request):
    res = function.show_all(request)
    return render_json(res)

def select_log(request):
    res = function.select_log(request)
    return render_json(res)

def select_rules_pagination(request):
    alert_rules = function.select_rules_pagination(request)
    return render_json(alert_rules)

def select_all_rules(request):
    alert_rules = function.select_all_rules(request)
    return render_json(alert_rules)

def select_Keyword(request):
    res = function.select_Keyword(request)
    return render_json(res)

def about_select(request):
    res = function.about_select(request)
    return render_json(res)

def about_search(request):
    res = function.about_search(request)
    return render_json(res)

def select_scenes(request):
    res = function.select_scenes(request)
    return render_json(res)