# -*- coding: utf-8 -*-
from db_connection.function import *
from django.core.paginator import *
from system_config.function import *
from custom_query.models import *
from datetime import datetime, timedelta


def select_queries_pagination(page_info):
    """
    分页获取自定义查询
    :param page_info:
    :return:
    """
    result_dict = dict()
    list_set = list()
    search = page_info['search']
    page = page_info['page']
    limit = page_info['limit']
    if None is not search and '' != search:
        queries_list = TbCustQuery.objects.filter(query_name__contains=search).all()
    else:
        queries_list = TbCustQuery.objects.all()
    paginator = Paginator(queries_list, limit)
    try:
        selected_set = paginator.page(page)
    except PageNotAnInteger:
        selected_set = paginator.page(1)
    except EmptyPage:
        selected_set = paginator.page(paginator.num_pages)
    for selected_data in selected_set:
        temp = model_to_dict(selected_data)
        list_set.append(temp)
    result_dict['items'] = list_set
    result_dict['pages'] = paginator.num_pages
    return result_dict


def del_query(query_data):
    """
    根据id删除自定义查询
    :param query_data:
    :return:
    """
    TbCustQuery.objects.filter(id=query_data['id']).delete()
    return "ok"


def select_query(query_data):
    """
    根据id获取自定义查询
    :param query_data:
    :return:
    """
    custom_query = TbCustQuery.objects.filter(id=query_data['id']).get()
    selected_query = model_to_dict(custom_query)
    return selected_query


def add_query(query_data):
    """
    添加 / 修改自定义查询
    :param query_data:
    :return:
    """
    status_dic = dict()
    print query_data
    TbCustQuery(**query_data).save()
    items_count = TbCustQuery.objects.count()
    pages = items_count // 5
    if 0 != items_count % 5:
        pages = pages + 1
    status_dic['message'] = 'ok'
    status_dic['total_pages'] = pages
    print 'PAGES: %s' % pages
    return status_dic


def sql_test(res):
    """
    根据sqltest查询出结果集
    :param res:
    :return:
    """
    try:
        conn = getAny_db(res['conn_id'])
        sql = res['sql']
        cursor = conn.cursor()  # 获取游标
        cursor.execute(sql)
        infos = cursor.fetchall()
        datas = []
        col = cursor.description
        names = []
        # 得到结果集的列名
        for c in col:
            names.append(c[0])
        # 根据列名生成对应列名的数据，排除datetime中的两种类型，避免转json出错
        for info in infos:
            data = {}
            for i in range(len(names)):
                if type(info[i]) == timedelta:
                    data[names[i]] = str(info[i])
                elif type(info[i]) == datetime:
                    data[names[i]] = datetime.strftime(info[i], "%Y-%m-%d %H:%M:%S")
                else:
                    data[names[i]] = info[i]
            datas.append(data)
        res = {
            'data': datas,
            'result': 'success'
        }
    except Exception as e:
        res = {
            'result': 'error'
        }
    return res
