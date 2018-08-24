#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-8-1 13:12
# @Author  : Jerry Wang
# @Site    : 
# @File    : url.py
# @Software: PyCharm

from django.conf.urls import url, include
from jenpip import views

urlpatterns = [
    url(r'^$', views.index, name='environ'),
    url(r'^add/', views.add, name='add_environ'),
    # url(r'^manage/', views.manage, name='manage'),
    url(r'^delete/', views.env_del, name='del_environ'),
    url(r'^edit/', views.edit, name='edit_environ'),
    url(r'^save/', views.save, name='save_environ'),
    url(r'^update/',views.update,name="update_environ"),
    url(r'^testlb/',views.test_lb_status,name="test_lb_status"),
]