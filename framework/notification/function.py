# -*- coding: utf-8 -*-

from models import *
from django.core.paginator import *
from gather_data.models import *
from system_config.function import *
from position.models import *
from shell_app.tools import *


def select_rules_pagination(page_info):
    """

    :param page_info:
    :return:
    """
    result_dict = dict()
    list_set = list()
    search = page_info['search'].strip()
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
        # datetime类型不支持转换，取出来置空后在使用model_to_dict转换
        create_time = selected_data.create_time
        edit_time = selected_data.edit_time
        upper_limit = selected_data.upper_limit
        lower_limit = selected_data.lower_limit
        selected_data.create_time = None
        selected_data.edit_time = None
        selected_data.upper_limit = None
        selected_data.lower_limit = None
        temp = model_to_dict(selected_data)
        # 手动转换datetime类型的数据，放入dict中
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


def select_rule(rule_data):
    """
    根据id获取告警规则
    :param rule_data:
    :return:
    """
    alert_rule = TbAlertRule.objects.filter(id=rule_data['id']).get()
    # datetime与decimal类型不支持转换，取出来置空后在使用model_to_dict转换
    create_time = alert_rule.create_time
    edit_time = alert_rule.edit_time
    upper_limit = alert_rule.upper_limit
    lower_limit = alert_rule.lower_limit
    alert_rule.create_time = None
    alert_rule.edit_time = None
    alert_rule.upper_limit = None
    alert_rule.lower_limit = None
    selected_rule = model_to_dict(alert_rule)
    # 手动转换datetime和decimal类型的数据，放入dict中
    if create_time is None:
        selected_rule['create_time'] = ''
    else:
        selected_rule['create_time'] = create_time.strftime('%Y-%m-%d %H:%M:%S')
    if edit_time is None:
        selected_rule['edit_time'] = ''
    else:
        selected_rule['edit_time'] = edit_time.strftime('%Y-%m-%d %H:%M:%S')
    if upper_limit is None:
        selected_rule['upper_limit'] = ''
    else:
        selected_rule['upper_limit'] = str(upper_limit)
    if lower_limit is None:
        selected_rule['lower_limit'] = ''
    else:
        selected_rule['lower_limit'] = str(lower_limit)
    return selected_rule


def del_rule(rule_data):
    """
    根据ID删除告警规则
    :param rule_data:
    :return:
    """
    user_count = TlAlertUser.objects.filter(rule_id=rule_data['id']).count()
    # 判断该告警规则是否被某用户订阅，如果已被用户订阅，先让用户确认是否强制删除
    if 0 != user_count:
        return "restrict"
    else:
        TbAlertRule.objects.filter(id=rule_data['id']).delete()
        return "ok"


def force_del_rule(rule_data):
    """
    根据ID强制删除告警规则
    :param rule_data:
    :return:
    """
    # 删除该用户订阅该告警规则的记录
    TlAlertUser.objects.filter(rule_id=rule_data['id']).delete()
    # 删除该告警规则
    TbAlertRule.objects.filter(id=rule_data['id']).delete()
    return "ok"


def add_rule(rule_data):
    """
    告警规则添加
    :param rule_data:
    :return:
    """
    status_dic = dict()
    # print rule_data
    TbAlertRule(**rule_data).save()
    # 获取当前数据总条数
    items_count = TbAlertRule.objects.count()
    # 获取当前的总页数
    pages = items_count // 5
    if 0 != items_count % 5:
        pages = pages + 1
    status_dic['message'] = 'ok'
    status_dic['total_pages'] = pages
    print 'PAGES: %s' % pages
    return status_dic


def is_data_alert(upper_limit, lower_limit, data_value):
    """
    判断当前数据是否超出限制，返回告警标志位alert_flag
    :param upper_limit:
    :param lower_limit:
    :param data_value:
    :return:
    """
    alert_flag = False
    # print 'UPPER_LIMIT: %s, LOWER_LIMIT: %s' % (selected_rule.upper_limit, selected_rule.lower_limit)
    # 告警规则配置了上限值和下限值的情况
    if upper_limit is not None and lower_limit is not None:
        if float(data_value) > upper_limit or float(data_value) < lower_limit:
            # print 'FIELD : %s, ALERT!!!!! VALUE %s OUT OF RANGE' % (data.data_key, data.data_value)
            alert_flag = True
    # 告警规则仅配置了上限值的情况
    elif upper_limit is not None and lower_limit is None:
        if float(data_value) > upper_limit:
            # print 'FIELD : %s, ALERT!!!!! VALUE %s OUT OF RANGE' % (data.data_key, data.data_value)
            alert_flag = True
    # 告警规则仅配置了下限值的情况
    elif upper_limit is None and lower_limit is not None:
        if float(data_value) < lower_limit:
            # print 'FIELD : %s, ALERT!!!!! VALUE %s OUT OF RANGE' % (data.data_key, data.data_value)
            alert_flag = True
    return alert_flag


def rule_check(monitor_id):
    """

    :param monitor_id:
    :return:
    """
    print 'monitor_id=%s-----Rule checking....' % monitor_id
    # 告警信息
    alert_infos = list()
    # 告警标志位
    alert_flag = False
    # 获取当前监控项下的所有采集数据
    gather_data = TDGatherData.objects.filter(item_id=monitor_id).all()
    for data in gather_data:
        selected_rule_count = TbAlertRule.objects.filter(item_id=data.item_id, key_name=data.data_key).count()
        # 如果当前采集数据有对应的告警规则，且为单值的情况，校验采集的数据
        if 0 != selected_rule_count and ',' not in data.data_value:
            selected_rule = TbAlertRule.objects.filter(item_id=data.item_id, key_name=data.data_key).get()
            # 校验当前数据是否告警
            alert_flag = is_data_alert(selected_rule.upper_limit, selected_rule.lower_limit, data.data_value)
            # 如果告警标志位为True生成告警信息
            if alert_flag:
                # 获取当前告警时间
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 搜集告警信息
                alert_info = dict()
                alert_info['rule_id'] = selected_rule.id
                alert_info['item_id'] = data.item_id
                alert_info['alert_time'] = now
                alert_info['alert_title'] = selected_rule.alert_title
                alert_info['alert_content'] = selected_rule.alert_content
                alert_info['staff_user'] = list()
                alert_user_results = TlAlertUser.objects.filter(rule_id=selected_rule.id).all()
                for alert_user in alert_user_results:
                    alert_info['staff_user'].append(alert_user.user_id)
                alert_infos.append(alert_info)
        else:
            print 'INFO: Multiple value or no matching rules, rule check skip.......'
    # 如果搜集到了告警信息，将alert_infos对象传递给celery并通知处理告警
    # print len(alert_infos)
    if 0 != len(alert_infos):
        pass
        # 邮箱被封暂时不能用了 send_alert(**alert_info)
        # 是否使用微信告警? wechat_alert(alert_infos)
    return "ok"


def send_alert(**msg):
    """

    :param msg:
    :return:
    """
    alert_title = msg['alert_title']
    alert_content = msg['alert_content']
    staff_users_ids = msg['staff_user']
    msg.update({'persons': msg.pop("staff_user")})
    print msg
    receivers = []
    for id in staff_users_ids:
        eml = user_info.objects.get(id=id).email
        receivers.append(eml)
    print receivers
    mail_send(alert_title, alert_content, receivers)
    TdAlertLog.objects.create(**msg)


def wechat_alert(msgs):
    """
    发送微信告警
    :param msgs:
    :return:
    """
    for msg in msgs:
        alert_title = msg['alert_title']
        alert_content = msg['alert_content']
        staff_users_ids = msg['staff_user']
        access_token = wechat_access_token()
        alert_msg = alert_title + '\n' + alert_content
        for id in staff_users_ids:
            open_id = user_info.objects.get(id=id).open_id
            wechat_send_msg(access_token, open_id, alert_msg)
        msg.update({'persons': msg.pop("staff_user")})
        TdAlertLog.objects.create(**msg)
