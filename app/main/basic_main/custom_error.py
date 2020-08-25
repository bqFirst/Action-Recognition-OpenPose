#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/1 9:34
# @Author : wangweimin
# @File   : custom_error.py
# @Desc   :


class MyCustomError(Exception):
    pass


class UserOperatorError(MyCustomError):
    """
    欲删除不可删除对象（或有挂钩数据的对象）
    模型操作
    上传错误类型数据，上传excel未及时操作
    """

    def __init__(self, *args):
        self.args = args


class RequestIdError(MyCustomError):

    def __init__(self, *args):
        self.args = args


class RequestUrlError(MyCustomError):

    def __init__(self, *args):
        self.args = args


class RequestValueError(MyCustomError):

    def __init__(self, *args):
        self.args = args


class NameRepeatedError(MyCustomError):

    def __init__(self, *args):
        self.args = args


class DatabaseConnectError(MyCustomError):

    def __init__(self, *args):
        self.args = args


class DatabaseSelectError(MyCustomError):

    def __init__(self, *args):
        self.args = args


class FileNotExistError(MyCustomError):

    def __init__(self, *args):
        self.args = args


class DataSrcNameError(MyCustomError):
    """
    读取工程数据时，工程数据名称不存在
    """

    def __init__(self, *args):
        self.args = args


class ServerError(MyCustomError):

    def __init__(self, *args):
        self.args = args


class DataParsingError(MyCustomError):
    """
    数据解析失败
    """

    def __init__(self, *args):
        self.args = args


class PortExhaustionError(MyCustomError):
    """
    开放端口被用完
    """

    def __init__(self, *args):
        self.args = args


class ParameterError(MyCustomError):

    def __init__(self, *args):
        self.args = args


class DockerContainerPredictError(MyCustomError):

    def __init__(self, *args):
        self.args = args


class DockerContainerNotFoundError(MyCustomError):

    def __init__(self, *args):
        self.args = args


class DockerContainerStartUpError(MyCustomError):

    def __init__(self, *args):
        self.args = args


class DockerContainerCheckError(MyCustomError):

    def __init__(self, *args):
        self.args = args


class DockerImageNotFoundError(MyCustomError):

    def __init__(self, *args):
        self.args = args


class ApplicationStopError(MyCustomError):

    def __init__(self, *args):
        self.args = args
