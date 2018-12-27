from django.shortcuts import render
import function
from common.mymako import render_json, render_mako_context


# Create your views here.

def index(request):

    return render_mako_context(request, 'show_message.html')


def unit_show(request):

    res = function.unit_show(request)
    return render_json(res)


def edit_unit(request):

    res = function.edit_unit(request)
    return render_json(res)

