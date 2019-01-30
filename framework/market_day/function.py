#!usr/bin/ebv python
# -*- coding:utf-8 -*-
from models import Holiday
import os
from xlrd import open_workbook
from framework.conf import default

def get_holiday(req):
    dates=Holiday.objects.filter(flag=0).values('day')
    days=[]
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
            workbook=open_workbook(path)
            sheet=workbook.sheet_by_index(0)
            for i in range(1,sheet.nrows):
                day = str(sheet.row_values(i)[0])
                d = day[0:4] + u'/' + str(int(day[4:6])) + u'/' + str(int(day[6:8]))
                flag=int(sheet.row_values(i)[1])
                holiday=Holiday(day=d,flag=flag)
                holiday.save()
        except:
            print '文件不匹配'

def delall(req):
    flag=Holiday.objects.all().delete()
    return flag

def delone(req,date):
    print date
    print Holiday.objects.filter(day=date)
    flag=Holiday.objects.filter(day=date).update(flag=1)
    print flag
    return flag

def addone(req,date):
    flag = Holiday.objects.filter(day=date).update(flag=0)
    return flag

def addschedules():
    default