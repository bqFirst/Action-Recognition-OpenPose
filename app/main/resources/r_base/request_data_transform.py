#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/29 20:18
# @Author : wangweimin
# @File   : request_data_transform.py
# @Desc   :

import json
import pandas as pd

from app.main.basic_main.custom_error import RequestValueError
from app.main.basic_main.error_message import ErrorMsg


def str2dict(data: json):
    data: dict = json.loads(data)
    if not isinstance(data, dict):
        raise TypeError('Json data required')
    return data


def str2pd(value: json):
    data: list = json.loads(value)
    if not isinstance(data, list):
        raise TypeError('A DataFrame is Required')
    data = pd.DataFrame(data)
    if not isinstance(data, pd.DataFrame):
        raise TypeError('A DataFrame is Required')
    return data


def str2int(value: str) -> int:
    """
    url请求中数据id转化为int型数据
    :param value:
    :return:
    """
    try:
        return int(value)
    except Exception:
        raise RequestValueError('Url请求出错')
