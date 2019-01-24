#!usr/bin/ebv python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from celery import task
from django.core.mail import send_mail
from django.conf import settings
from time import sleep

@task
def sendemail(email):
    sleep(5)
    send_mail('subject','here is message',settings.DEFAULT_FROM_EMAIL,[email],fail_silently=False)
    return 'success'