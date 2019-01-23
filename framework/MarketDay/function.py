#!usr/bin/ebv python
# -*- coding:utf-8 -*-
from MarketDay.models import *
import os

def get_holiday(req):
    dates=Holiday.objects.all().values('day')
    days=[]
    for date in dates:
        days.append(date['day'])
    print days
    return days

def get_file(req):
    if req.method == 'POST':
        try:
            obj = req.FILES.get('file')
            filename = obj.name
            path = os.getcwd() + r'\\static\\dateTxt\\' + filename
            print path
            if not os.path.exists(path):
                with open(path, 'wb')as f:
                    for chunk in obj.chunks():
                        f.write(chunk)
                f.close()
            f=open(path,'r')
            strall=f.read()
            strs=strall.split(',')
            for str in strs:
                holiday=Holiday(day=str)
                holiday.save()
        except:
            print '文件不匹配'

def delall(req):
    flag=Holiday.objects.all().delete()
    return flag

def delone(req,date):
    flag=Holiday.objects.get(day=date).delete()
    return flag
