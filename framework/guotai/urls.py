# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from guotai.views import *

urlpatterns = [
    url(r'^index/$', home),
    url(r'^$', home),
    url(r'^base_index$', base_index),
    url(r'^test/$', test),
]
