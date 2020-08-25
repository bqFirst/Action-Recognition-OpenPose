#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/23 16:39
# @Author : wangweimin
# @File   : application_socketio_operator.py
# @Desc   :

from app.main.services.operator.base_common.websocket_operator.websocket_operator import WebSocketService


class ApplicationSocketIOService(object):

    @staticmethod
    def refresh(application_id: int, address: str):
        WebSocketService.emit(event='refresh', address=address, application_id=application_id)
