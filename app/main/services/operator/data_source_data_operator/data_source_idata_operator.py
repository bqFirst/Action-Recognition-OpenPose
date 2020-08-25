#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/7 8:55
# @Author : wangweimin
# @File   : data_source_idata_operator.py
# @Desc   :

from abc import abstractmethod, ABCMeta


class DsIDataService(object, meteaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def __allowed_file(filename: str):
        pass

    @classmethod
    @abstractmethod
    def upload(cls, f, data_name: str, catalog_id: int, user_id: int, data_type: str, project_id: int):
        pass

    @classmethod
    @abstractmethod
    def rename(cls, data_link_id: int, catalog_id: int, new_name: str):
        pass

    @classmethod
    @abstractmethod
    def delete(cls, data_link_id: int, is_forced=False) -> bool:
        pass

    @classmethod
    @abstractmethod
    def overview(cls, data_link_id: int, data_type: str) -> list:
        pass

    @classmethod
    @abstractmethod
    def get(cls, data_link_id: int, data_type: str, page: int, limit: int):
        pass
