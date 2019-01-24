#!usr/bin/ebv python
# -*- coding:utf-8 -*-
from MarketDay.models import *
import os
from xlrd import open_workbook

def get_holiday(req):
    dates=Holiday.objects.filter(flag=0).values('day')
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
            workbook=open_workbook(path)
            sheet=workbook.sheet_by_index(0)
            for i in range(sheet.nrows):
                day = str(sheet.row_values(i)[0])
                d = day[0:4] + u'/' + day[4:6] + u'/' + day[6:8]
                print d
                flag=int(sheet.row_values(i)[1])
                holiday=Holiday(day=str,flag=flag)
                holiday.save()
        except:
            print '文件不匹配'

def delall(req):
    flag=Holiday.objects.all().delete()
    return flag

def delone(req,date):
    flag=Holiday.objects.get(day=date).delete()
    return flag

def addone(req,date):
    holiday=Holiday(day=date)
    flag=holiday.save()
    return flag
