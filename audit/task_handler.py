#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-7-17 20:31
# @Author  : Jerry Wang
# @Site    : 
# @File    : task_handler.py
# @Software: PyCharm
import json
import os
import subprocess
from audit import models
from django.conf import settings
from django.db.transaction import atomic


class Task(object):
    """
    处理批量任务，包括命令和文件传输
    """
    def __init__(self,request):
        self.request = request
        self.errors = []
        self.task_data = None
        self.cmd_type = 0
        self.random_str = None

    def is_valid(self):
        """
        1、验证命令、主机列表合法
        :return:
        """
        task_data = self.request.POST.get("task_data")

        if task_data:
            self.task_data = json.loads(task_data)
            print(self.task_data.get("lange_id"),555)
            if self.task_data.get("lange_id") == "python":
                self.cmd_type = 1
            else:
                self.cmd_type = 0
            if self.task_data.get("task_type") == "cmd":
                if self.task_data.get("cmd") and self.task_data.get("selected_host_ids"):
                    return True
                self.errors.append({"invalid_argument": "cmd or host_list is empty"})
            elif self.task_data.get("task_type") == "file_transfer":
                self.errors.append({"invalid_argument": "cmd or host_list is empty"})
            else:
                self.errors.append({"invalid_argument": "task_type is invalid"})
        self.errors.append({"invalid_data":"task_data is not exist"})

    def run(self,random_str):
        """
        start task ,and return task id
        :return:
        """
        task_func = getattr(self,self.task_data.get("task_type"))
        print(task_func)
        task_id = task_func(random_str)
        return task_id


    def cmd(self,random_str):
        """
        批量任务
        :return:
        """
        print("cmd multi task....")
        content = self.task_data.get("cmd")
        print(content,self.cmd_type)
        print(111,self.request.user.account.id,self.task_data.get("cmd"))
        task_obj = models.Task.objects.create(
            task_type = 0,
            cmd_type = self.cmd_type,
            account_id = self.request.user.account.id,
            content = self.task_data.get("cmd"),
        )
        task_obj.save()
        host_ids = set(self.task_data.get("selected_host_ids"))
        tasklog_objs = []
        for host_id in host_ids:
            tasklog_objs.append(
                models.TaskLog(task_id=task_obj.id,
                               host_user_bind_id = host_id,
                               status = 3)
            )
        # 初始化
        models.TaskLog.objects.bulk_create(tasklog_objs,100)

        from django import db
        db.close_old_connections()
        # task_obj.host_user_binds.add(*self.task_data.get("selected_host_ids"))
        # task_obj.save()
        cmd_str = u"python %s %s %s %s" % (settings.MULTI_TASK_SCRIPT,task_obj.id,self.cmd_type,random_str)
        if self.cmd_type == 0:
            cmd_arg = "sh"
        else:
            cmd_arg = "py"

        cmd_file = "/opt/LuffyClient/%s.%s" % (task_obj.id, cmd_arg)
        print(random_str)
        upload_to = os.path.join(settings.FILE_UPLOADS, str(task_obj.account.id), random_str)
        if not os.path.isdir(upload_to):
            os.makedirs(upload_to, exist_ok=True)
        f = open(os.path.join(upload_to, "%s.%s" % (task_obj.id, cmd_arg)), 'wb')
        f.write(content.encode("utf-8"))
        f.close()
        print(cmd_str)

        multitask_obj = subprocess.Popen(cmd_str,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
        print("task result :", multitask_obj.stdout.read(), multitask_obj.stderr.read().decode('gbk'))
        return task_obj

    def file_transfer(self):
        """批量文件"""

        task_obj = models.Task.objects.create(
            task_type = 1,
            account = self.request.user.account ,
            content = json.dumps(self.task_data),
            #host_user_binds =
        )
        tasklog_objs = []
        host_ids = set(self.task_data.get("selected_host_ids"))
        for host_id in host_ids:
            tasklog_objs.append(
                models.TaskLog(task_id=task_obj.id,
                               host_user_bind_id=host_id,
                               status = 3
                               )
            )
        models.TaskLog.objects.bulk_create(tasklog_objs,100)

        cmd_str = "python %s %s" % (settings.MULTI_TASK_SCRIPT,task_obj.id)
        multitask_obj = subprocess.Popen(cmd_str,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE )
        # print("task result :",multitask_obj.stdout.read(),multitask_obj.stderr.read().decode('gbk'))
        # print(cmd_str)
        return task_obj