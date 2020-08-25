#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/15 10:48
# @Author : wangweimin
# @File   : websocket_response.py
# @Desc   :


class WebSocketResponse(object):

    RefreshResponse = {'code': 4}
    LogResponse = {'code': 6}

    @classmethod
    def refresh(cls, **kwargs) -> dict:
        res = cls.RefreshResponse.copy()
        res.update(kwargs)
        return res

    @classmethod
    def log(cls, **kwargs) -> dict:
        res = cls.LogResponse.copy()
        res.update(kwargs)
        return res
