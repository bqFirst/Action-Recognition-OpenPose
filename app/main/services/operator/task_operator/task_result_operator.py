#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/4 8:50
# @Author : wangweimin
# @File   : task_result_operator.py
# @Desc   :

from app import db
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.data_base_operator.data_cale import get_data_link_record
from app.main.services.operator.base_common.object_operator.object_acquisition import ObjectAcquisition
from app.models import TaskResultFile
from conf.data_path import DataDirectoryPath


class TaskResultService(object):

    @staticmethod
    def delete(result_data_id: int):
        result_data: TaskResultFile = TaskResultFile.query.get(result_data_id)
        if result_data is None:
            return
        DataFileOperator(address='application').delete(file_name=result_data.alias)
        db.session.delete(result_data)
        db.session.commit()

    @classmethod
    def get(cls, result_data_id: int, page: int, limit: int):
        result_data: TaskResultFile = ObjectAcquisition.task_result_file_by_id(result_data_id)
        data = DataFileOperator(address='application').get(filename=result_data.alias,
                                                           paging={'start': page * limit, 'nrows': limit})
        return data, get_data_link_record(result_data)

    @classmethod
    def download(cls, result_data_id: int):
        result_data: TaskResultFile = ObjectAcquisition.task_result_file_by_id(result_data_id)
        filename: str = result_data.name
        suffix: str = 'csv'
        if '.' not in filename:
            filename = filename + '.' + suffix

        return DataDirectoryPath.get_application_path(), result_data.alias, filename
