import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import function
from common.mymako import render_json, render_mako_context


# Create your views here.

def index(request):

    return render_mako_context(request, './monitorScene/senceSet.html')


# def index1(request):
#
#     return render_mako_context(request, '123.html')


@csrf_exempt
def monitor_show(request):

    res = function.monitor_show(request)
    return render_json(res)


# @csrf_exempt
# def select_unit(request):
#
#     res = function.select_unit(request)
#     return render_json(res)
#
#
# @csrf_exempt
# def edit_unit(request):
#
#     function.edit_unit(request)
#     return render_json(None)
#
#
# @csrf_exempt
# def delete_unit(request):
#
#     function.delete_unit(request)
#     return render_json(None)

