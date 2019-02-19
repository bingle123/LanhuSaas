# -*- coding: utf-8 -*-
from django.shortcuts import render
from common.mymako import render_json
from common.mymako import render_mako_context


def show_index(request):
    return render_mako_context(request, './alertRuleManage/alertRuleManage.html')