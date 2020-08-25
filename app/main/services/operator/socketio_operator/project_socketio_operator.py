#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/23 15:31
# @Author : wangweimin
# @File   : project_socketio_operator.py
# @Desc   :

from app.main.services.operator.base_common.websocket_operator.websocket_operator import WebSocketService


class ProjectSocketIOService(object):

    @staticmethod
    def refresh(project_id: int, address: str):
        WebSocketService.emit(event='refresh', address=address, project_id=project_id)
