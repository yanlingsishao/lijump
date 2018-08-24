#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-7-18 14:39
# @Author  : Jerry Wang
# @Site    : 
# @File    : tasks.py
# @Software: PyCharm

from LuffyAudit.celery import app
from celery import task


# @task
# def kk():
#     from .backend import multitask
#     multitask.jj()
#     print("lala")

# @app.task
# def hello_world():
#     print('Hello World')