#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/22 16:41
# @Author : wangweimin
# @File   : __init__.py.py
# @Desc   : 面向切面编程


class Test(object):
    # 通过初始化方法，将要被装饰的函数传进来并记录下来
    def __init__(self, func):
        self.__func = func

    # 重写 __call__ 方法来实现装饰内容
    def __call__(self, *args, **kwargs):
        print('wrapper context')
        self.__func(*args, **kwargs)
