#!usr/bin/ebv python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from celery import task
from django.core.mail import send_mail
from django.conf import settings
from time import sleep
from celery.task import periodic_task
@task
def sendemail(email):
    sleep(5)
    send_mail('i come from china','go to you',settings.DEFAULT_FROM_EMAIL,[email],fail_silently=False)
    return 'success'
@task
def mul(x,y):
    return x*y