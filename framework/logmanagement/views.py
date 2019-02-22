# encoding:utf-8
import function
from common.mymako import render_json, render_mako_context


# Create your views here.

def index(request):
    return render_mako_context(request, './monitor/show_message.html')

def add_log(request):
    res = function.add_log(request)
    return render_json(res)


