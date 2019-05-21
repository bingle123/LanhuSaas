#!usr/bin/ebv python
# -*- coding:utf-8 -*-
from models import Holiday, HeaderData, Area
import os
# from xlrd import open_workbook
from monitor_item.models import Monitor
from django.forms import model_to_dict
from django.db.models import Q
import celery_opt as co
import json
from datetime import datetime
import pytz
from shell_app.function import get_user
from settings import BK_PAAS_HOST


def get_holiday(req, area):
    dates = Holiday.objects.filter(Q(flag=0) & Q(area=int(area))).values('day')
    days = []
    for date in dates:
        days.append(date['day'])
    return days


# 通过节假日文件获取节假日
def get_file(req, area):
    """

    :param req:
    :param area:
    :return:
    """
    if req.method == 'POST':
        try:
            obj = req.FILES.get('file')
            filename = obj.name
            path = os.getcwd() + r'\\static\\' + filename
            if not os.path.exists(path):
                with open(path, 'wb')as f:
                    for chunk in obj.chunks():
                        f.write(chunk)
                f.close()
            # workbook = open_workbook(path)
            workbook = None
            sheet = workbook.sheet_by_index(0)
            delall(area)
            for i in range(1, sheet.nrows):
                day = str(sheet.row_values(i)[0])
                d = day[0:4] + u'/' + str(int(day[4:6])) + u'/' + str(int(day[6:8]))
                flag = int(sheet.row_values(i)[1])
                holiday = Holiday(day=d, flag=flag, area=area)
                holiday.save()
        except:
            print '文件不匹配'


def delall(area):
    """
    删除所有的节假日
    :param area:
    :return:
    """
    flag = Holiday.objects.filter(area=int(area)).delete()
    return flag


def delone(req):
    """
    删除指定的节假日
    :param req:
    :return:
    """
    res = json.loads(req.body)
    date = res['date']
    area = res['area']
    flag = Holiday.objects.filter(Q(day=date) & Q(area=int(area))).update(flag=1)
    return flag


def addone(req):
    """
    添加一个日志为节假日
    :param req:
    :return:
    """
    res = json.loads(req.body)
    date = res['date']
    area = res['area']
    day = Holiday.objects.get(Q(day=date) & Q(area=int(area)))
    day.flag = 0
    day.save()
    return 'ok'


def addperdic_task():
    """
    定时任务demo
    :return:
    """
    flag = co.create_task_interval(name='demo_per', task='market_day.tasks.count_time', task_args=[10, 50],
                                   desc='demodemo', interval_time={'every': 10, 'period': 'seconds'})
    return flag


def add_unit_task(add_dicx):
    """
    添加一个监控项定时任务
    :param add_dicx:
    :return:
    """
    type = add_dicx['monitor_type']
    print type
    schename = add_dicx['monitor_name']
    id = Monitor.objects.filter(monitor_name=schename).last().id
    schename = str(id)
    starthour = str(add_dicx['start_time']).split(':')[0]
    startmin = str(add_dicx['start_time']).split(':')[1]
    endtime = add_dicx['end_time']
    # 创建一个特定时区的时间的实例
    temp_date = datetime(2019, 2, 12, int(starthour), int(startmin), 0)
    timezone = Area.objects.get(id=add_dicx['monitor_area']).timezone
    # 将开始时间转化为对应时区的时间
    starthour, startmin = tran_time_china(temp_date, timezone=timezone)
    temp_date = datetime(2019, 2, 12, int(endtime.split(':')[0]), int(endtime.split(':')[1]), 0)
    endhour, endmin = tran_time_china(temp_date, timezone=timezone)
    endtime = endhour + ":" + endmin
    period = int(add_dicx['period'])
    if type == 1:
        ctime = {
            'hour': starthour,
            'minute': startmin,
        }
        info = {
            'id': id,
            'gather_params': add_dicx['gather_params'],
            'params': add_dicx['params'],
            'gather_rule': add_dicx['gather_rule'],
            'period': period,
            'area_id': add_dicx['monitor_area'],
            'task_name': str(schename) + 'task',
            'endtime': endtime,
            'score':add_dicx['score'],
            'key':add_dicx['measure_name'],
            'gather_type':add_dicx['display_type'],
            'display_rule':add_dicx['display_rule']
        }
        # 创建一个基本监控项采集的开始任务
        co.create_task_crontab(name=schename, task='market_day.tasks.gather_data_task_one', crontab_time=ctime,
                               task_args=info, desc=schename)
    # elif type == 2:
    #     ctime = {
    #         'hour': starthour,
    #         'minute': startmin,
    #     }
    #     info = {
    #         'id': id,
    #         'gather_params': 'sql',
    #         'params': add_dicx['params'],
    #         'gather_rule': add_dicx['gather_rule'],
    #         'period': period,
    #         'area_id': add_dicx['monitor_area'],
    #         'task_name': str(schename) + 'task',
    #         'endtime': endtime
    #     }
    #     # 创建一个图标采集开始任务
    #     co.create_task_crontab(name=schename, task='market_day.tasks.gather_data_task_one', crontab_time=ctime,
    #                            task_args=info, desc=schename)
    #
    # elif type == 3:
    #     ctime = {
    #         'hour': starthour,
    #         'minute': startmin,
    #     }
    #     info = {
    #         'id': id,
    #         'params': add_dicx['params'],  # ip
    #         'gather_params': add_dicx['gather_params'],
    #         'job_id': [{
    #             'name': add_dicx['gather_rule'],
    #             'id': add_dicx['jion_id']
    #         }],
    #         'period': period,
    #         'area_id': add_dicx['monitor_area'],
    #         'task_name': str(schename) + 'task',
    #         'endtime': endtime
    #     }
    #     # 创建一个作业采集的开始任务
    #     co.create_task_crontab(name=schename, task='market_day.tasks.gather_data_task_two', crontab_time=ctime,
    #                            task_args=info, desc=schename)
    # elif type == 'fourth':
    #     template_list = add_dicx['jion_id']
    #     node_times = add_dicx['node_times']
    #     constants = add_dicx['constants']
    #     ctime = {
    #         'hour': starthour,
    #         'minute': startmin,
    #     }
    #     info = {
    #         'id': id,
    #         'template_id': template_list,  # 创建任务的模板id
    #         'node_times': node_times,
    #         'period': period,
    #         'constants': constants,
    #         'area_id': add_dicx['monitor_area'],
    #         'task_name': str(schename) + 'task',
    #         'endtime': endtime
    #     }
    #     # 创建一个开始流程的任务
    #     co.create_task_crontab(name=schename, task='market_day.tasks.start_flow_task', crontab_time=ctime,
    #                            task_args=info, desc=schename)
    elif type ==5:
        ctime = {
            'hour': starthour,
            'minute': startmin,
        }
        info = {
            'id': id,
            'gather_params': add_dicx['gather_params'],
            'params': add_dicx['params'],
            'gather_rule': add_dicx['gather_rule'],
            'period': period,
            'area_id': add_dicx['monitor_area'],
            'task_name': str(schename) + 'task',
            'endtime': endtime,
            'score': add_dicx['score'],
            'source_type': add_dicx['source_type'],
            'target_name': add_dicx['target_name'],
            'measure_name': add_dicx['measure_name'],
            'dimension': add_dicx['dimension'],
            'display_type': add_dicx['display_type'],
            'display_rule': add_dicx['display_rule'],
        }
        co.create_task_crontab(name=schename, task='market_day.tasks.gather_data_task_five', crontab_time=ctime,
                               task_args=info, desc=schename)


def get_header_data(request):
    """
    获取蓝鲸平台的头文件，并存入数据库
    :param request:
    :return:
    """
    role_id = get_user(request)['data']['bk_role']
    h, flag = HeaderData.objects.get_or_create(id=1)
    headers = {
        "Content-Type": 'application/json;charset=utf-8',
        "Cookie": 'csrftoken=bNAyZ7pBsJ1OEi8TMq1NqxNXY2CUREEO; sessionid=r9g2ofn1wb0ykd1epg8crk9l5pgyeuu2; bk_csrftoken=GdxslZh1U3YVsCthqXIv09PbVoW0AaQd; bklogin_csrftoken=z8goJXIMXil80lFT3VtLQHMClrPIExl9; blueking_language=zh-cn; bk_token=kxgoYlRp77AkbGVX85AdFVR0t6eqqHeJ-BlMXxA6oM0',
        "Host": BK_PAAS_HOST,
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3679.0 Safari/537.36',
        "X-CSRFToken": 'FI1fszvZzgIsYYX8n6aPMduEeAL7qTV3',
        "X-Requested-With": 'XMLHttpRequest'
    }
    csrftoken = request.COOKIES["csrftoken"];
    Cookie = "keyA=1";
    for key in request.COOKIES:
        Cookie = "%s;%s=%s" % (Cookie, key, request.COOKIES[key]);
    headers["Cookie"] = Cookie;
    headers["X-CSRFToken"] = csrftoken;
    # 如果当前用户不是管理员无法访问v3接口不保存header信息
    if role_id == 1:
        h.header = json.dumps(headers, ensure_ascii=False)
        h.save()


def add_area(req):
    """
    添加一个新的日历地区
    :param req:
    :return:
    """
    res = json.loads(req.body)
    name = res['country']
    timezone = res['timezone']
    a, flag = Area.objects.get_or_create(country=name)
    a.timezone = timezone
    a.save()
    return 'ok'


def get_all_area(req):
    """
    获取所有的日历地区
    :param req:
    :return:
    """
    areas = Area.objects.all()
    area_dict = []
    for a in areas:
        area_dict.append(model_to_dict(a))
    return area_dict


def del_area(name):
    """
    删除日历的某个地区
    :param name:
    :return:
    """
    Area.objects.get(id=name).delete()
    Holiday.objects.filter(area=name).delete()
    return 'ok'


def get_all_timezone():
    """
    获得世界上的所有时区
    :return:
    """
    all = pytz.common_timezones
    return all


def check_jobday(id):
    """
    判断今天是不是对应地区的工作日
    :param id:
    :return:
    """
    timezone = Area.objects.get(id=id).timezone
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    str_date = datetime.strftime(now, '%Y/%m/%d')
    day = str_date[:4] + u'/' + str(int(str_date[5:7])) + u'/' + str(int(str_date[8:10]))
    hs = Holiday.objects.filter(Q(day=day) & Q(area=id))
    flag = 0
    for h in hs:
        flag = h.flag
    if flag == 1:
        return True
    else:
        return False


def tran_time_china(tempdate, timezone):
    """
    将不同时区的时间转为中国时间
    :param tempdate:
    :param timezone:
    :return:
    """
    central = pytz.timezone('Asia/Shanghai')
    local_us = central.localize(tempdate)
    # 使用astimezone得出时间
    time = local_us.astimezone(pytz.timezone(timezone))
    return str(time.hour), str(time.minute)


def tran_china_time_other(time, timezone):
    """
    将中国时间转为不同的时区
    :param time:
    :param timezone:
    :return:
    """
    hour = time.hour
    min = time.minute
    tempdate = datetime(2019, 1, 2, int(hour), int(min), 0)
    timezone = Area.objects.get(id=timezone).timezone
    central = pytz.timezone(timezone)
    local_us = central.localize(tempdate)
    # 使用astimezone得出时间
    time = local_us.astimezone(pytz.timezone('Asia/Shanghai'))
    return str(time.hour) + ":" + str(time.minute)
