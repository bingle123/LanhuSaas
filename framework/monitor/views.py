from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import function
from common.mymako import render_json, render_mako_context


# Create your views here.

def index(request):

    return render_mako_context(request, 'show_message.html')


def index1(request):

    return render_mako_context(request, '123.html')


def unit_show(request):

    res = function.unit_show(request)
    return render_json(res)

@csrf_exempt
def select_unit(request):

    res = function.select_unit(request)
    return render_json(res)


def delete_unit(request):
    pass

