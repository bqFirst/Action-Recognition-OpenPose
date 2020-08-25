#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/30 14:48
# @Author : wangweimin
# @File   : data_transform.py
# @Desc   :

import datetime
import time


def datetime2timestamp(data: datetime.datetime) -> float:
    if data is None:
        return 1565137700
    return time.mktime(data.timetuple())
