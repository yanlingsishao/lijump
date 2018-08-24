#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-8-14 9:48
# @Author  : Jerry Wang
# @Site    : 
# @File    : 1.py
# @Software: PyCharm
import paramiko

ssh = paramiko.SSHClient()
key = paramiko.AutoAddPolicy()
ssh.set_missing_host_key_policy(key)
ssh.connect('192.168.1.52', 22, 'root', 'huazhen@123' ,timeout=5)
stdin, stdout, stderr = ssh.exec_command('python print 11')
result = stdout.read() + stderr.read()
print(result)