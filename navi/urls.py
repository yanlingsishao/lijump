#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-7-31 19:31
# @Author  : Jerry Wang
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url, include
from navi import views

urlpatterns = [
    url(r'^$', views.index, name='navi'),
    url(r'^add/', views.add, name='add'),
    # url(r'^manage/', views.manage, name='manage'),
    url(r'^delete/', views.delete, name='environ_del'),
    # url(r'^edit/', views.edit, name='edit'),
    # url(r'^save/', views.save, name='save'),
]