#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-6-26 18:40
# @Author  : Jerry Wang
# @Site    : 
# @File    : server.py
# @Software: PyCharm
import gevent
import paramiko
import json
from gevent.socket import wait_read,wait_write
from . import models


def add_log(user,content,log_type="1"):
    try:
        models.AccessLog.objects.create(
            user=user,
            log_type=log_type,
            content=content
        )
    except Exception as e:
        print("保存日志过程中发生了错误:",e)


class WSSHBridge:
    """
    桥接websocket 和 SSH的核心类
    :param hostname:
    :param port:
    :param username:
    :param password:
    :return:
    """
    def __init__(self,websocket,user):
        self.user = user
        self._websocket = websocket
        self._tasks = []
        self.trans = None
        self.channel = None
        self.cptext = ''
        self.cmd_string = ''

    def open(self,hostname,port=22,username=None,password=None):
        """
        建立SSH连接
        :param host_ip:
        :param port:
        :param username:
        :param password:
        :return:
        """
        try:
            self.trans = paramiko.Transport(hostname,port)
            self.trans.start_client()
            self.trans.auth_password(username=username,password=password)
            channel = self.trans.open_session(timeout=60)
            channel.get_pty()
            self.channel = channel
        except Exception as e:
            self._websocket.send(json.dumps({"error":e}))
            raise

    def _forward_inbound(self,channel):
        """
        正向数据转发，websocket -> ssh
        :param channel:
        :return:
        """
        try:
            while True:
                data = self._websocket.receive()

                if not data:
                    return
                data = json.loads(str(data))

                # data["data"] = data["data"] + "2"

                if "data" in data:
                    self.cmd_string += data["data"]
                    channel.send(data["data"])
        finally:
            self.close()

    def _forword_outbound(self,channel):
        """
        反向数据转发，ssh -> websocket
        :param channel:
        :return:
        """
        try:
            while True:
                wait_read(channel.fileno())

                data = channel.recv(65535)
                if not len(data):
                    return

                self._websocket.send(json.dumps({"data":data.decode()}))
        finally:
            self.close()

    def _bridge(self,channel):
        channel.setblocking(False)
        channel.settimeout(0.0)
        self._tasks = [
            gevent.spawn(self._forward_inbound,channel),
            gevent.spawn(self._forword_outbound, channel),
        ]
        gevent.joinall(self._tasks)

    def close(self):
        """
        结束会话
        :return:
        """
        gevent.killall(self._tasks,block=True)
        self._tasks = []

    def shell(self):
        """
        启动一个shell通信界面
        :return:
        """
        self.channel.invoke_shell()
        self._bridge(self.channel)
        self.channel.close()
        # 创建日志
        add_log(self.user,self.cmd_string,)





