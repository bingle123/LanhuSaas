# -*- coding: utf-8 -*-
from __future__ import division
from logmanagement.models import *
from django.core.paginator import *
from system_config.function import *
from notification.models import *
def show_all(request):
    """
        显示所有操作日志
    """
    res = json.loads(request.body)
    limit = res['limit']
    page = res['page']
    log = Operatelog.objects.all()
    p = Paginator(log, limit)
    count = p.page_range
    pages = count[-1]
    res_list = []
    current_page = p.page(page)
    for x in current_page:
        dic = {
            'id': x.id,
            'log_type': x.log_type,
            'log_name': x.log_name,
            'user_name': x.user_name,
            'class_name': x.class_name,
            'method': x.method,
            'create_time': str(x.create_time),
            'succeed': x.succeed,
            'message': x.message,
            'page_count': pages
        }
        res_list.append(dic)
    return  res_list


def select_all_rules():
    alert_rules = TbAlertRule.objects.order_by('item_id').all()
    rule_list = []
    for alert_rule in alert_rules:
        create_time = alert_rule.create_time
        edit_time = alert_rule.edit_time
        upper_limit = alert_rule.upper_limit
        lower_limit = alert_rule.lower_limit
        alert_rule.create_time = None
        alert_rule.edit_time = None
        alert_rule.upper_limit = None
        alert_rule.lower_limit = None
        temp = model_to_dict(alert_rule)
        if create_time is None:
            temp['create_time'] = ''
        else:
            temp['create_time'] = create_time.strftime('%Y-%m-%d %H:%M:%S')
        if edit_time is None:
            temp['edit_time'] = ''
        else:
            temp['edit_time'] = edit_time.strftime('%Y-%m-%d %H:%M:%S')
        if upper_limit is None:
            temp['upper_limit'] = ''
        else:
            temp['upper_limit'] = str(upper_limit)
        if lower_limit is None:
            temp['lower_limit'] = ''
        else:
            temp['lower_limit'] = str(lower_limit)
        rule_list.append(temp)
    return rule_list


# 分页获取告警规则
def select_rules_pagination(page_info):
    result_dict = dict()
    list_set = list()
    search = page_info['search']
    page = page_info['page']
    limit = page_info['limit']
    if None is not search and '' != search:
        rules_list = TbAlertRule.objects.filter(rule_name__contains=search).all()
    else:
        rules_list = TbAlertRule.objects.all()
    paginator = Paginator(rules_list, limit)
    try:
        selected_set = paginator.page(page)
    except PageNotAnInteger:
        selected_set = paginator.page(1)
    except EmptyPage:
        selected_set = paginator.page(paginator.num_pages)
    for selected_data in selected_set:
        create_time = selected_data.create_time
        edit_time = selected_data.edit_time
        upper_limit = selected_data.upper_limit
        lower_limit = selected_data.lower_limit
        selected_data.create_time = None
        selected_data.edit_time = None
        selected_data.upper_limit = None
        selected_data.lower_limit = None
        temp = model_to_dict(selected_data)
        if create_time is None:
            temp['create_time'] = ''
        else:
            temp['create_time'] = create_time.strftime('%Y-%m-%d %H:%M:%S')
        if edit_time is None:
            temp['edit_time'] = ''
        else:
            temp['edit_time'] = edit_time.strftime('%Y-%m-%d %H:%M:%S')
        if upper_limit is None:
            temp['upper_limit'] = ''
        else:
            temp['upper_limit'] = str(upper_limit)
        if lower_limit is None:
            temp['lower_limit'] = ''
        else:
            temp['lower_limit'] = str(lower_limit)
        list_set.append(temp)
    result_dict['items'] = list_set
    result_dict['pages'] = paginator.num_pages
    return result_dict

# def select_Keyword(request):
#     res = json.loads(request.body)
#     limit = res['limit']
#     page = res['page']
#     search = res['search'].strip()
#     res1 = search
#     res_list = []
#     tmp = Operatelog.objects.all()
#     log = tmp.filter(Q(log_type__icontains=res1) | Q(log_name__icontains=res1) | Q(user_name__icontains=res1) | Q(
#         class_name__icontains=res1) | Q(method__icontains=res1))
#     p = Paginator(log, limit)
#     count = p.page_range
#     pages = count[-1]
#     current_page = p.page(page)
#     for x in current_page:
#         dic = {
#             'id': x.id,
#             'log_type': x.log_type,
#             'log_name': x.log_name,
#             'user_name': x.user_name,
#             'class_name': x.class_name,
#             'method': x.method,
#             'create_time': str(x.create_time),
#             'succeed': x.succeed,
#             'message': x.message,
#             'page_count': pages
#         }
#         res_list.append(dic)
#     return res_list

def select_log(request):
    res = json.loads(request.body)
    limit = res['limit']
    page = res['page']
    search = res['search'].strip()
    res1 = search
    res2 = res['keyword']
    print res1
    print res2
    res_list = []
    tmp = Operatelog.objects.all()
    if(res1 != ""):
        log = tmp.filter(Q(log_type__icontains=res1))
    elif(res2 != ""):
        log = tmp.filter(Q(log_name__icontains=res2) | Q(user_name__icontains=res2) | Q(
        class_name__icontains=res2) | Q(method__icontains=res2))
    elif(res1 != "" & res2 != ""):
        log = tmp.filter(Q(log_type__icontains=res1) & Q(log_name__icontains=res2) | Q(user_name__icontains=res2) | Q(
            class_name__icontains=res2) | Q(method__icontains=res2))
    p = Paginator(log, limit)
    count = p.page_range
    pages = count[-1]
    current_page = p.page(page)
    for x in current_page:
        dic = {
            'id': x.id,
            'log_type': x.log_type,
            'log_name': x.log_name,
            'user_name': x.user_name,
            'class_name': x.class_name,
            'method': x.method,
            'create_time': str(x.create_time),
            'succeed': x.succeed,
            'message': x.message,
            'page_count': pages
        }
        res_list.append(dic)
    return res_list
