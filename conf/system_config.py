#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/31 15:56
# @Author : wangweimin
# @File   : system_config.py
# @Desc   :

import os
import sys

from conf.data_path import DataDirectoryPath


Settings = {
    'docker.ip': '127.0.0.1',  # 相对与flask服务器位置
}


class PylintCommand(object):
    """
    环境必须安装pylint
    """

    Command: str = None

    @classmethod
    def init(cls):
        system: str = sys.platform
        if system.startswith('linux'):
            cls.Command = os.path.join(DataDirectoryPath.get_package_path(), 'venv', 'bin', 'pylint')
        else:
            cls.Command = 'pylint'

    @classmethod
    def command(cls) -> str:
        if cls.Command is None:
            cls.init()
        return cls.Command


class ServerAddress(object):
    """flask服务器启动地址，异步框架celery需要范文"""

    Address: str = ''

    @classmethod
    def init(cls, config_name: str):
        if 'production' == config_name:
            cls.Address = '172.16.0.194:9090'
        else:
            cls.Address = '127.0.0.1:5000'

    @classmethod
    def get_address(cls):
        if not cls.Address:
            raise ValueError
        return cls.Address
