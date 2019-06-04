#!usr/bin/ebv python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from celery import task,shared_task
from system_config.function import test
from celery.task import periodic_task
from gather_data import function
from monitor_item import tools
from celery.schedules import crontab
import market_day.celery_opt as co
from account.models import BkUser
from blueking.component.shortcuts import get_client_by_user
from datetime import datetime
from custom_process.function import clear_execute_status
from market_day.function import check_jobday
from monitor_item.models import *
from history_chart.function import select_scene_operation
from iqube_interface.gather import Gather
import json
from common.log import logger
from common.mymako import render_json
from gather_data.function import gather_data_save,gather_data_migrate


@task
def crawl_task(**i):
    print u'爬虫开始'
    test()
    return 'success'


# 基本监控项和图表监控项的采集开始task
@shared_task
def gather_data_task_one(**i):
    # 启动一个
    area_id = i['area_id']
    period = {
        'every': i['period'],
        'period': 'seconds'
    }
    task_name = i['task_name']
    info = {
        'id': i['id'],
        'gather_params': i['gather_params'],
        'params': i['params'],
        'gather_rule': i['gather_rule'],
        'task_name': i['task_name'],
        'endtime': i['endtime'],
        'score':i['score']
    }
    logger.error(u"celery 调用数据采集任务：{}".format(datetime.now()))
    if check_jobday(area_id):
        co.create_task_interval(name=task_name, task='market_day.tasks.basic_monitor_task', interval_time=period,
                                task_args=info, desc=task_name)

    else:
        pass


# 基本监控项的采集任务
@task(ignore_result=True)
def basic_monitor_task(**i):
    # 调用基本监控项和图标监控项数据采集的方法
    endtime = i['endtime']
    task_name = i['task_name']
    # 逾期删除本任务
    strnow = datetime.strftime(datetime.now(), '%H:%M')
    if strnow <= endtime:
        logger.error(u"celery 调用数据库采集任务：{}".format(datetime.now()))
        function.gather_data(**i)
    else:
        co.delete_task(task_name)


@shared_task
def gather_data_task_five(**add_dicx):
    """
    一体化平台的采集开始任务
    :param i:
    :return:
    """
    area_id = add_dicx['area_id']
    period = {
        'every': add_dicx['period'],
        'period': 'seconds'
    }
    task_name = add_dicx['task_name']
    info = add_dicx
    if check_jobday(area_id):
        co.create_task_interval(name=task_name, task='market_day.tasks.base_monitor_task', interval_time=period,
                                task_args=info, desc=task_name)
    else:
        pass


@task(ignore_result=True)
def base_monitor_task(**i):
    endtime = i['endtime']
    task_name = i['task_name']
    # 逾期删除本任务
    strnow = datetime.strftime(datetime.now(), '%H:%M')
    if strnow <= endtime:
        # 调用一体化监控项数据采集的方法
        logger.error(u"celery 调用一体化平台采集任务：{}".format(datetime.now()))
        interface_type = "measures"
        measures = i['target_name']
        measures_name = i['measure_name']
        show_rule_type = i['display_type']
        gather_rule = i['gather_rule']
        str = '{hostname=*}'
        for dimension_obj in json.loads(i['dimension']):
            key = dimension_obj['dimension_name']
            value = dimension_obj['dimension_value']
        str += '{' + key + '=' + value + '}'
        # 执行数据采集入库
        result_info = {
            'type': "add",
            'measures': "",
            'item_id': i['id'],
            'score': i['score']
        }

        try:
            res = Gather.gather_base_test(interface_type=interface_type, measures=measures, measures_name=measures_name,
                                     show_rule_type=show_rule_type, gather_rule=gather_rule, interface_param=str)
            # 取得一体化平台采集结果
            result = render_json(res)
            result_info['measures'] = result.results
            # 数据迁移
            gather_data_migrate(i['id'])
            gather_data_save(result_info)
        except Exception as e:
            result_info['measures'] = ""
            # 数据迁移
            gather_data_migrate(i['id'])
            result_info['score'] = 0
            gather_data_save(result_info)
    else:
        print u'删除' + task_name
        co.delete_task(task_name)

@task
def count_time(**i):
    """
    定时任务测试
    :param i:
    :return:
    """
    return i['x'] * i['y']


def clear_status_task():
    """
    定时清理定制流程状态任务
    :return:
    """
    clear_execute_status()


def select_scene_operation_task():
    """

    :return:
    """
    select_scene_operation()
