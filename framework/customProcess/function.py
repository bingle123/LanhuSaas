# -*- coding: utf-8 -*-

from models import *
from django.forms.models import model_to_dict


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
        status.do_time = ''
        status.do_person = ''
        status.save()
    return "ok"
