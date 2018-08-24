#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-6-14 17:05
# @Author  : Jerry Wang
# @Site    : 
# @File    : user_interactive.py
# @Software: PyCharm
from django.contrib.auth import authenticate
from django.conf import settings
import subprocess,random,string
from audit import models

class UserShell(object):
    """
    用户登录堡垒机后的Shell
    """
    def __init__(self,sys_argv):
        self.sys_argv = sys_argv
        self.user = None

    def auth(self):
        count = 0
        while count < 3:
            username = input("username:").strip()
            password = input("password:").strip()
            user = authenticate(username=username,password=password)
            # None 代表认证不成功
            # User object 返回user对象  user.name
            if not user:
                count += 1
                print("Invalid username or password")
            else:
                self.user = user
                return True
        else:
            print("尝试太多次")

    def start(self):
        """启动交互程序"""

        if self.auth():
            # print(self.user.account.host_user_binds.all()) #select_related()
            while True:
                host_groups = self.user.account.host_groups.all()
                for index, group in enumerate(host_groups):
                    print("         %s.\t%s[%s]" % (index, group, group.host_user_binds.count()))
                print("         %s.\t未分组机器[%s]" % (len(host_groups), self.user.account.host_user_binds.count()))
                try:
                    choice = input("select group>:").strip()
                    if choice.isdigit():
                        choice = int(choice)
                        host_bind_list = None
                        if choice >= 0 and choice < len(host_groups):
                            selected_group = host_groups[choice]
                            host_bind_list = selected_group.host_user_binds.all()
                        elif choice == len(host_groups):  # 选择的未分组机器
                            # selected_group = self.user.account.host_user_binds.all()
                            host_bind_list = self.user.account.host_user_binds.all()
                        if host_bind_list:
                            while True:
                                for index, host in enumerate(host_bind_list):
                                    print("         %s.\t%s" % (index, host.host,))
                                choice2 = input("select host>(b返回上级):").strip()
                                if choice2.isdigit():
                                    choice2 = int(choice2)
                                    if choice2 >= 0 and choice2 < len(host_bind_list):
                                        selected_host = host_bind_list[choice2]
                                        #print("selected host", selected_host)
                                        s = string.ascii_lowercase + string.digits
                                        random_tag = ''.join(random.sample(s, 10))
                                        session_obj = models.SessionLog.objects.create(account=self.user.account,
                                                                                       host_user_binds=selected_host)
                                        cmd = "/usr/local/bin/sshpass -p '%s' /usr/local/openssh/bin/ssh %s@%s -p %s -o StrictHostKeyChecking=no -Z %s" % (
                                        selected_host.host_user.password, selected_host.host_user.username,
                                        selected_host.host.ip_addr,
                                        selected_host.host.port,
                                        random_tag
                                        )
                                        session_tracker_script = "/bin/sh %s %s %s" % (
                                        settings.SESSION_TRACKER_SCRIPT, random_tag, session_obj.id)
                                        session_tracker_obj = subprocess.Popen(session_tracker_script, shell=True,
                                                                               stdout=subprocess.PIPE,
                                                                               stderr=subprocess.PIPE)
                                        # print(session_tracjer_obj.stdout.read(),session_tracjer_obj.stderr.read())
                                        #print("2")
                                        ssh_channel = subprocess.run(cmd, shell=True)
                                        print("select host>(b返回上级):")
                                        #print(ssh_channel.stdout.read(),ssh_channel.stderr.read())
                                elif choice2 == 'b':
                                    break
                except KeyboardInterrupt  as e:
                    pass
