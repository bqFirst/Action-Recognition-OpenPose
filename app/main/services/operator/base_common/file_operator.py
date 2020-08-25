#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/7 10:08
# @Author : wangweimin
# @File   : file_operator.py
# @Desc   :

import os

from app.main.services.core.basic.uuid_name import get_uuid_name
from conf.data_path import DataDirectoryPath


class FileWrite(object):

    def __init__(self, address: str):
        self.directory = None

        if not self.set_directory(address=address):
            raise NotADirectoryError(
                'ERROR: Can\'t find directory, please apply correct parameter address')

    def set_directory(self, address: str) -> bool:
        if 'data_source' == address:
            self.directory: str = DataDirectoryPath.get_data_source_path()
            return True
        elif 'src' == address:
            self.directory = DataDirectoryPath.get_model_src_path()
            return True
        else:
            return False

    def write(self, f, alias: str) -> str:
        alias_path = os.path.join(self.directory, alias)
        try:
            f.save(alias_path)
            return alias
        except Exception as e:
            if os.path.exists(alias):
                os.remove(alias)
            raise


def file_write_service(f, address: str) -> str:
    """
    :param f: 文件流
    :param address: 文件地址
        address='data_source' 表示文件流写入数据源目录
        address='src' 表示文件流写入模型源码目录
    :return: bool, filename
    """
    file_write = FileWrite(address=address)
    filename = f.filename
    if '.' in filename:
        alias = get_uuid_name(suffix=f.filename.split('.')[-1])
    else:
        alias = get_uuid_name('unknown')
    return file_write.write(f=f, alias=alias)
