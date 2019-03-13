# -*- coding: utf-8 -*-


from common.mymako import render_json, render_mako_context
import function

def get_time(request):
    res = function.get_time(request)
    return render_json(res)

def scenes_alert(request):
    res = function.scenes_alert(request)
    return render_json(res)