# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'db_connection_manage.views',
    (r'^$', 'index'),
)
