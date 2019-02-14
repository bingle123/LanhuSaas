# -*- coding: utf-8 -*-
from django.shortcuts import render
from common.mymako import render_json
from common.mymako import render_mako_context
from . import function
import json


def gather_data(request):
    info = json.loads(request.body)
    status = function.gather_data(info)
    return render_json(status)

