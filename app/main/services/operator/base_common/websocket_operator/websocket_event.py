#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/26 9:17
# @Author : wangweimin
# @File   : websocket_event.py
# @Desc   :


class WebSocketEvent(object):

    @staticmethod
    def refresh() -> str:
        return 'refresh'

    @staticmethod
    def log() -> str:
        return 'log'
