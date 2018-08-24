#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-8-14 18:08
# @Author  : Jerry Wang
# @Site    : 
# @File    : test2.py
# @Software: PyCharm
import os,sys
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) )
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LuffyAudit.settings")

    import django
    django.setup()

    from audit import models
    z = models.Task.objects.all()
    for i in z:
        print(i.id)