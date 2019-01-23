import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import function
from common.mymako import render_json, render_mako_context


# Create your views here.

def index(request):
    return render_mako_context(request, './jobManagement/jobM.html')

@csrf_exempt
def positonall(request):
    res = function.job_show(request)
    return render_json(res)

@csrf_exempt
def select_job(request):
    res = function.select_job(request)
    return render_json(res)

@csrf_exempt
def delete_job(request):
    function.delete_job(request)
    return render_json(None)

@csrf_exempt
def add_job(request):
    function.add_job(request)
    return render_json(0)

@csrf_exempt
def add_person(request):
    function.add_person(request)
    return render_json(0)

@csrf_exempt
def edit_job(request):
    r = function.edit_job(request)
    return render_json(r)

@csrf_exempt
def get_user(request):
    r = function.get_user(request)
    return render_json(r)