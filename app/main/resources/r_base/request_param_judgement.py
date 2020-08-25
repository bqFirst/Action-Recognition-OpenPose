#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/3 15:26
# @Author : wangweimin
# @File   : request_param_judgement.py
# @Desc   :

import numpy as np

from app.main.basic_main.custom_error import RequestValueError


def one_and_the_only(*args):
    if 1 != np.sum(np.array(args) != None):
        raise RequestValueError('Error id')
