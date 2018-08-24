#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-6-14 17:02
# @Author  : Jerry Wang
# @Site    : 
# @File    : audit_shell.py
# @Software: PyCharm

import sys,os


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LuffyAudit.settings")
    import django
    django.setup() # 手动注册django所有的APP
    from audit.backend import user_interactive

    obj = user_interactive.UserShell(sys.argv)
    obj.start()
