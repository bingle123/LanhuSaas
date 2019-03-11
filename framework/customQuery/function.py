# -*- coding: utf-8 -*-

from models import *
from django.forms.models import model_to_dict
from db_connection.models import *
from db_connection.function import *
from django.core.paginator import *
import MySQLdb
from system_config.function import *
from customQuery.models import *


# 分页获取自定义查询
def select_queries_pagination(page_info):
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


# 根据id删除自定义查询
def del_query(query_data):
    TbCustQuery.objects.filter(id=query_data['id']).delete()
    return "ok"


# 根据id获取自定义查询
def select_query(query_data):
    custom_query = TbCustQuery.objects.filter(id=query_data['id']).get()
    selected_query = model_to_dict(custom_query)
    return selected_query


# 添加 / 修改自定义查询
def add_query(query_data):
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


# 根据数据库ID获取当前数据库中的所有表信息
def load_all_tables_name(db):
    status = dict()
    conn_info = Conn.objects.filter(id=db['conn_id']).get()
    db_name = conn_info.databasename
    if 'MySQL' == conn_info.type:
        query_sql = 'select table_name from information_schema.tables where table_schema="%s"' % db_name
    elif 'Oracle' == conn_info.type:
        query_sql = 'select table_name from user_tables'
    elif 'SQL Server' == conn_info.type:
        query_sql = 'select name as table_name from sysobjects where xtype="U"'
    else:
        raise RuntimeError(u'不支持的数据库类型')
    conn = getAny_db(db['conn_id'])
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query_sql)
    res = cursor.fetchall()
    status['message'] = 'ok'
    status['names'] = res
    return status


# 根据表名查询当前表所有字段信息
def load_all_fields_name(tb):
    status = dict()
    fields = list()
    if -1 == tb['tables_name'].find(','):
        table_names = list()
        table_names.append(tb['tables_name'])
    else:
        table_names = tb['tables_name'].split(',')
    conn_info = Conn.objects.filter(id=tb['conn_id']).get()
    conn = getAny_db(tb['conn_id'])
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    db_name = conn_info.databasename
    for table_name in table_names:
        if 'MySQL' == conn_info.type:
            query_sql = 'select column_name from information_schema.COLUMNS where table_name = "%s" and table_schema="%s"' % (table_name, db_name)
        elif 'Oracle' == conn_info.type:
            query_sql = 'select column_name from user_tab_columns where table_name=upper("%s")' % table_name
        elif 'SQL Server' == conn_info.type:
            query_sql = 'select syscolumns.name as column_name from syscolumns where id=object_id("%s")' % table_name
        else:
            raise RuntimeError(u'不支持的数据库类型')
        cursor.execute(query_sql)
        res = cursor.fetchall()
        fields.extend(res)
    status['message'] = 'ok'
    status['fields'] = fields
    return status

#根据sqltest查询出结果集
def sql_test(res):
    conn = getAny_db(res['conn_id'])
    sql=res['sql']
    cursor = conn.cursor()  # 获取游标
    cursor.execute(sql)
    infos=cursor.fetchall()
    datas=[]
    col=cursor.description
    names=[]
    for c in col:
        names.append(c[0])
    for info in infos:
        data={}
        for i in range(len(names)):
            data[names[i]]=info[i]
        datas.append(data)
    return datas

