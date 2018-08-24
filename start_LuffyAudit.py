#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-6-26 14:06
# @Author  : Jerry Wang
# @Site    : 
# @File    : start_LuffyAudit.py
# @Software: PyCharm
import os
import argparse
from gevent import monkey;monkey.patch_all()


from gevent.pywsgi import WSGIServer

from geventwebsocket.handler import WebSocketHandler
from LuffyAudit.wsgi import application


version = "1.0.0"

root_path = os.path.dirname(__file__)


parser = argparse.ArgumentParser(
    description="LuffyAudit - 基于WebSocket的堡垒机"
)

parser.add_argument('--port','-p',
                    type=int,
                    default=8000,
                    help="服务器端口，默认为8000")

parser.add_argument('--host','-H',
                    default="0.0.0.0",
                    help='服务器IP，默认为0.0.0.0')

args = parser.parse_args()

print('LuffyAudit{0} running on {1}:{2}'.format(version,args.host,args.port))
print((args.host,args.port))
ws_server = WSGIServer(
    (args.host,args.port),
    application,
    log=None,
    handler_class=WebSocketHandler,
)

try:
    ws_server.serve_forever()
except KeyboardInterrupt:
    print("服务器关闭")

