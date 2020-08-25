#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/30 15:39
# @Author : wangweimin
# @File   : error_message.py
# @Desc   :

import threading

from app.models import ErrorMessage


class ErrorMsg(object):
    ERROR: dict = {}
    Lock = threading.Lock()

    @classmethod
    def init(cls):
        cls.Lock.acquire()
        try:
            if cls.ERROR:
                return
            error_messages: list = ErrorMessage.query.all()
            for error_message in error_messages:
                cls.ERROR[error_message.id] = error_message.message
        except Exception:
            raise
        finally:
            cls.Lock.release()

    @classmethod
    def get_error_message(cls, error_id: int) -> str:
        msg: str = cls.ERROR.get(error_id)
        if msg is None:
            cls.init()
            msg: str = cls.ERROR.get(error_id)
        return msg
