# -*- coding: utf-8 -*-

from models import TbCustProcess
from django.forms.models import model_to_dict



def select_all_nodes():
    node_info = TbCustProcess.objects.order_by('seq').all()
    node_list = []
    for node in node_info:
        dic = model_to_dict(node)
        node_list.append(dic)
    return node_list


def add_node(node):
    TbCustProcess(**node).save()
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