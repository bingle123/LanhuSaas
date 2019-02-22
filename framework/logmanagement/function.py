# -*- coding: utf-8 -*-
from __future__ import division
from django.db.models import Q
from django.core.paginator import Paginator
import datetime

def add_log(request):
    res = json.loads(request.body)
    log_type = res['log_type']
    log_name = res['log_name']
    tmp = get_active_user(request)
    nowPerson = tmp['data']['bk_username']
    rl = JobInstance.objects.create(log_type=log_type,user_name=nowPerson,)