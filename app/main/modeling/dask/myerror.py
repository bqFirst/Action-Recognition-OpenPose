#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/18 9:56
# @Author : wangweimin
# @File   : myerror.py
# @Desc   :


class CreateDaskClusterError(Exception):

    def __init__(self, *args):
        self.args = args
