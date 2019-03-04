#!usr/bin/ebv python
# -*- coding:utf-8 -*-
from djcelery import models as celery_models
import json


def create_task_crontab(name, task, task_args, crontab_time, desc):
    """
    新增定时任务
    :param name: 定时任务名称
    :param task: 对应tasks里已有的task
    :param task_args: list 参数
    {"x":1, "Y":1}
    :param crontab_time: 时间配置
    {
        'month_of_year': 9  # 月份
        'day_of_month': 5   # 日期
        'hour': 01         # 小时
        'minute':05  # 分钟
    }
    :param desc: 定时任务描述
    :return: True or False
    """

    # task任务， created是否定时创建
    task, created = celery_models.PeriodicTask.objects.get_or_create(name=name, task=task)
    # 获取 crontab
    crontab = celery_models.CrontabSchedule.objects.filter(**crontab_time).first()
    if crontab is None:
        # 如果没有就创建，有的话就继续复用之前的crontab
        crontab = celery_models.CrontabSchedule.objects.create(**crontab_time)
    task.crontab = crontab  # 设置crontab
    if created:
        task.enabled = False # 开启task
    task.kwargs = json.dumps(task_args, ensure_ascii=False) # 传入task参数
    task.description = desc
    task.save()
    return True


def create_task_interval(name, task, task_args,interval_time, desc):
    """
    新增定时任务
    :param name: 定时任务名称
    :param task: 对应tasks里已有的task
    :param task_args: list 参数
    [arg1,arg2]
    :param crontab_time: 时间配置
    {
        'every':10,
        'period':'seconds'
    }
    :param desc: 定时任务描述
    :return: True or False
    """

    # task任务， created是否定时创建
    task, created = celery_models.PeriodicTask.objects.get_or_create(name=name, task=task)
    # 获取 crontab
    interval = celery_models.IntervalSchedule.objects.filter(**interval_time).first()
    if interval is None:
        # 如果没有就创建，有的话就继续复用之前的crontab
        interval = celery_models.IntervalSchedule.objects.create(**interval_time)
    task.interval=interval  # 设置crontab
    if created:
        task.enabled = True # 开启task
    task.kwargs=json.dumps(task_args, ensure_ascii=False) #将kwargs传入
    task.description = desc
    task.save()
    return True


def change_task_status(name,crontab_time,args):
    """
    任务状态切换：open or close
    :param name: 任务名称
    :param mode: 模式
    :param crontab_time: 时间配置
    {
        'month_of_year': 9  # 月份
        'day_of_month': 5   # 日期
        'hour': 01         # 小时
        'minute':05  # 分钟
    }
    :return: True or False
    """
    try:
        task = celery_models.PeriodicTask.objects.get(name=name)
        # 获取 crontab
        crontab = celery_models.CrontabSchedule.objects.filter(**crontab_time).first()
        if crontab is None:
            # 如果没有就创建，有的话就继续复用之前的crontab
            crontab = celery_models.CrontabSchedule.objects.create(**crontab_time)
        task.crontab = crontab  # 设置crontab
        task.kwargs = json.dumps(args, ensure_ascii=False)  # 将kwargs传入
        task.save()
        return True
    except celery_models.PeriodicTask.DoesNotExist:
        return False

def disable_task(name):
    """
    关闭任务
    """
    try:
        task = celery_models.PeriodicTask.objects.get(name=name)
        task.enabled = False  # 设置关闭
        task.save()
        print name+u'关闭成功'
        return True
    except celery_models.PeriodicTask.DoesNotExist:
        return False


def enable_task(name):
    """
    开启任务
    """
    try:
        task = celery_models.PeriodicTask.objects.get(name=name)
        task.enabled = True  # 设置开启
        task.save()
        print name+u'开启成功'
        return True
    except celery_models.PeriodicTask.DoesNotExist:
        return False


def delete_task(name):
    """
    根据任务名称删除任务
    :param name: task name
    :return: True or False
    """
    try:
        task = celery_models.PeriodicTask.objects.get(name=name)
        task.enabled = False  # 设置关闭
        task.delete()
        print name +u'删除成功'
        return True
    except celery_models.PeriodicTask.DoesNotExist:
        return False
