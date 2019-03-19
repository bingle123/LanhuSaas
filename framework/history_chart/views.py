# encoding:utf-8
import function
from common.mymako import render_json, render_mako_context


def index(request):
    """

    :param request:
    :return:
    """
    return render_mako_context(request, './history_chart/history.html')


def show_all(request):
    """

    :param request:
    :return:
    """
    res = function.show_all(request)
    return render_json(res)


def select_log(request):
    """

    :param request:
    :return:
    """
    res = function.select_log(request)
    return render_json(res)


def select_rules_pagination(request):
    """

    :param request:
    :return:
    """
    alert_rules = function.select_rules_pagination(request)
    return render_json(alert_rules)


def select_all_rules(request):
    """

    :param request:
    :return:
    """
    alert_rules = function.select_all_rules(request)
    return render_json(alert_rules)


def select_Keyword(request):
    """

    :param request:
    :return:
    """
    res = function.select_Keyword(request)
    return render_json(res)


def about_select(request):
    """

    :param request:
    :return:
    """
    res = function.about_select(request)
    return render_json(res)


def about_search(request):
    """

    :param request:
    :return:
    """
    res = function.about_search(request)
    return render_json(res)


def select_scenes(request):
    """

    :param request:
    :return:
    """
    res = function.select_scenes(request)
    return render_json(res)


def selectScenes_ById(request):
    """

    :param request:
    :return:
    """
    res = function.selectScenes_ById(request)
    return render_json(res)


def show_operation_report(request):
    """

    :param request:
    :return:
    """
    res = function.show_operation_report(request)
    return render_json(res)


def monthly_select(request):
    """

    :param request:
    :return:
    """
    res = function.monthly_select(request)
    return render_json(res)


def get_week(request):
    """

    :param request:
    :return:
    """
    res = function.get_week(request)
    return render_json(res)
