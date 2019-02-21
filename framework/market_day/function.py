#!usr/bin/ebv python
# -*- coding:utf-8 -*-
from models import Holiday
import os
from xlrd import open_workbook
from framework.conf import default
from monitor.models import Monitor
from django.forms import model_to_dict
import celery_opt as co
import tasks


def get_holiday(req):
    dates = Holiday.objects.filter(flag=0).values('day')
    days = []
    for date in dates:
        days.append(date['day'])
    return days


def get_file(req):
    if req.method == 'POST':
        try:
            obj = req.FILES.get('file')
            filename = obj.name
            path = os.getcwd() + r'\\static\\dateTxt\\' + filename
            if not os.path.exists(path):
                with open(path, 'wb')as f:
                    for chunk in obj.chunks():
                        f.write(chunk)
                f.close()
            workbook = open_workbook(path)
            sheet = workbook.sheet_by_index(0)
            for i in range(1, sheet.nrows):
                day = str(sheet.row_values(i)[0])
                d = day[0:4] + u'/' + str(int(day[4:6])) + u'/' + str(int(day[6:8]))
                flag = int(sheet.row_values(i)[1])
                holiday = Holiday(day=d, flag=flag)
                holiday.save()
        except:
            print '文件不匹配'


def delall(req):
    flag = Holiday.objects.all().delete()
    return flag


def delone(req, date):
    print date
    print Holiday.objects.filter(day=date)
    flag = Holiday.objects.filter(day=date).update(flag=1)
    print flag
    return flag


def addone(req, date):
    flag = Holiday.objects.filter(day=date).update(flag=0)
    return flag


def addperdic_task():
    flag=co.create_task_interval(name='demo_per', task='market_day.tasks.count_time', task_args=[10,50], desc='demodemo',interval_time={'every':10,'period':'seconds'})
    return flag

def add_unit_task(add_dicx):
    schename = add_dicx['monitor_name']
    type=add_dicx['monitor_type']
    print type
    id=Monitor.objects.get(monitor_name=schename).id
    if type=='基本单元类型' or type=='图表单元类型':
        starthour = str(add_dicx['start_time'])[:2]
        endhour = str(add_dicx['end_time'])[:2]
        period = int(add_dicx['period'])
        ctime = {
            'hour': starthour + '-' + endhour,
            'minute': '*/1',
        }
        info = {
            'id': id,
            'gather_params': add_dicx['gather_params'],
            'params': add_dicx['params'],
            'gather_rule': add_dicx['gather_rule'],
            'period':period
        }
        co.create_task_crontab(name=schename, task='market_day.tasks.gather_data_task_one', crontab_time=ctime,task_args=info, desc=schename)
    elif type=='作业单元类型':
        starthour = str(add_dicx['start_time'])[:2]
        endhour = str(add_dicx['end_time'])[:2]
        period = int(add_dicx['period'])
        ctime = {
            'hour': starthour + '-' + endhour,
            'minute':'*/1',
        }
        info = {
            'id': id,
            'params' : add_dicx['params'],  # ip
            'gather_params' : add_dicx['gather_params'],
            'job_id': [{
                'name': add_dicx['gather_rule'],
                'id': add_dicx['jion_id']
            }],
            'period':period
        }
        co.create_task_crontab(name=schename, task='market_day.tasks.gather_data_task_two', crontab_time=ctime,task_args=info, desc=schename)
    elif type=='流程单元类型':
        template_id=add_dicx['template_id']
        node_times=add_dicx['node_times']
        constants=add_dicx['constants']
        print node_times[-1]
        starthour = str(node_times[-1]['starttime']).split(':')[0]
        startmin = str(node_times[-1]['starttime']).split(':')[-1]
        ctime = {
            'hour': starthour,
            'minute': startmin,
        }
        info = {
            'id': id,
            'template_id': template_id,   #创建任务的模板id
            'node_times':node_times,
            'period':'period',
            'constants':constants
        }
        co.create_task_crontab(name=schename, task='market_day.tasks.start_flow_task', crontab_time=ctime,task_args=info, desc=schename)
