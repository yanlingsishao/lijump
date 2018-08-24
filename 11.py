#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-8-14 14:13
# @Author  : Jerry Wang
# @Site    : 
# @File    : 11.py
# @Software: PyCharm

def conn_sqllite(sql):
    import sqlite3
    con = sqlite3.connect("F:\LuffyAudit1\Luffy\Luffy\LuffyAudit\db.sqlite3")
    # 获得游标
    cur = con.cursor()
    # 查询整个表
    z = cur.execute(sql)
    return z


z = conn_sqllite("audit_task",'select * from ' + table + 'where id = ')
for i in z:
    print(i[0])