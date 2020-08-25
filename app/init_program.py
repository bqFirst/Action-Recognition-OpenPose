#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/8 8:46
# @Author : wangweimin
# @File   : init_program.py
# @Desc   :

from app.main.services.operator.base_common.docker_base_operator.docker_client import DockerClient
from conf.data_path import DataDirectoryPath


def init_program():
    DataDirectoryPath.init()
    DockerClient.init()
