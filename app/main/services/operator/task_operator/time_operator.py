#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/4 9:49
# @Author : wangweimin
# @File   : time_operator.py
# @Desc   :

import datetime


class TimeService(object):

    @staticmethod
    def to_str(datetime_: datetime.datetime=None):
        return datetime_.strftime('%Y/%m/%d %X.%f')[:-3]

    @classmethod
    def now_str(cls):
        return cls.to_str(datetime.datetime.now())

    @staticmethod
    def to_millisecond(second) -> str:
        millisecond = str(second * 1000)
        split = millisecond.split('.')
        return '.'.join([split[0], split[1][:3]])
