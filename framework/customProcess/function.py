# -*- coding: utf-8 -*-

from models import *
from position.models import *
from django.forms.models import model_to_dict
from shell_app.tools import *


def select_all_nodes():
    node_info = TbCustProcess.objects.order_by('seq').all()
    node_list = []
    for node in node_info:
        dic1 = model_to_dict(node)
        temp = TdCustProcessLog.objects.filter(node_id=node.id).get()
        do_time_ori = temp.do_time
        temp.do_time = None
        dic2 = model_to_dict(temp)
        # 由于model_to_dict方法不支持datetime类型的数据直接转换字典，手动转换
        if do_time_ori is None:
            dic2['do_time'] = ''
        else:
            dic2['do_time'] = do_time_ori.strftime('%Y-%m-%d %H:%M:%S')
        dic1['status'] = dic2
        node_list.append(dic1)
    return node_list


def add_node(node):
    TbCustProcess(**node).save()
    last_node = TbCustProcess.objects.last()
    has_record = TdCustProcessLog.objects.filter(node_id=last_node.id).count()
    if 0 == has_record:
        TdCustProcessLog(node_id=last_node.id).save()
    return "ok"


def select_all_bkusers():
    users_list = list()
    bk_users = Localuser.objects.all()
    for bk_user in bk_users:
        user_dict = model_to_dict(bk_user)
        users_list.append(user_dict)
    return users_list


def update_node_status(node):
    selected_status = TdCustProcessLog.objects.get(node_id=node['node_id'])
    selected_status.is_done = node['is_done']
    selected_status.do_time = node['do_time']
    selected_status.do_person = node['do_person']
    selected_status.save()
    return "ok"


def change_status_flag(node):
    selected_status = TdCustProcessLog.objects.get(node_id=node['node_id'])
    selected_status.is_done = node['is_done']
    selected_status.save()
    return "ok"


def del_node(node_id):
    TbCustProcess.objects.filter(id = node_id['id']).delete()
    return "ok"


def select_node(node_id):
    node = TbCustProcess.objects.filter(id = node_id['id']).get()
    node_list = []
    dic = model_to_dict(node)
    node_list.append(dic)
    return node_list


def truncate_node():
    TbCustProcess.objects.all().delete()
    return "ok"


def clear_execute_status():
    nodes_status = TdCustProcessLog.objects.all()
    for status in nodes_status:
        status.is_done = 'n'
        status.do_time = None
        status.do_person = None
        status.save()
    return "ok"


def send_notification(notification):

    send_flag = True

    status = dict()
    if -1 != notification['receivers'].find(','):
        receivers = notification['receivers'].split(',')
    else:
        receivers = list()
        receivers.append(notification['receivers'])
    infos = list()
    access_token = None
    sms_send_list = None
    mail_send_list = None
    for receiver in receivers:
        rec_info = Localuser.objects.filter(user_name=receiver).get()
        if 'wechat' == rec_info.notice_style:
            if None is access_token:
                access_token = wechat_access_token()
                if None is access_token:
                    print 'Wechat access token get fail'
                    send_flag = False
                    infos.append(u'微信接入Token获取异常!')
                    break
            res = wechat_send_msg(access_token, rec_info.open_id, notification['content'])
            if None is res:
                infos.append(u'%s: 微信通知发送成功!' % receiver)
            else:
                infos.append(u'%s: 微信通知发送失败! %s' % (receiver, res))
                send_flag = False
        elif 'sms' == rec_info.notice_style:
            if None is sms_send_list:
                sms_send_list = list()
            sms_send_list.append(receiver)
        elif 'email' == rec_info.notice_style:
            if None is sms_send_list:
                mail_send_list = list()
            mail_send_list.append(receiver)
    if None is not sms_send_list:
        pass
    if send_flag:
        status['message'] = 'ok'
    else:
        status['message'] = 'error'
    status['info'] = infos
    return status
