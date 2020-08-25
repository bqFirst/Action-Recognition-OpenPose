#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/10 16:36
# @Author : wangweimin
# @File   : websocket_operator.py
# @Desc   :

from app import socketio
from app.main.services.operator.base_common.websocket_operator.websocket_namespance import WebSocketNamespace
from app.main.services.operator.base_common.websocket_operator.websocket_response import WebSocketResponse
from app.main.services.operator.base_common.websocket_operator.websocket_event import WebSocketEvent


class WebSocketService(object):

    @classmethod
    def emit(cls, event: str, address: str, **kwargs):
        if 'log' == event:
            if 'task' == address:
                socketio.emit(WebSocketEvent.log(), WebSocketResponse.log(**kwargs),
                              namespace=WebSocketNamespace.task_log())
        elif 'refresh' == event:
            if 'process' == address:
                socketio.emit(WebSocketEvent.refresh(), WebSocketResponse.refresh(**kwargs),
                              namespace=WebSocketNamespace.project_process())
            elif 'model' == address:
                socketio.emit(WebSocketEvent.refresh(), WebSocketResponse.refresh(**kwargs),
                              namespace=WebSocketNamespace.project_model())
            elif 'task' == address:
                socketio.emit(WebSocketEvent.refresh(), WebSocketResponse.refresh(**kwargs),
                              namespace=WebSocketNamespace.app_task())
            elif 'application' == address:
                socketio.emit(WebSocketEvent.refresh(), WebSocketResponse.refresh(**kwargs),
                              namespace=WebSocketNamespace.app())
