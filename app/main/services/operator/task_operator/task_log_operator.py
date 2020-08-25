#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/4 8:50
# @Author : wangweimin
# @File   : task_log_operator.py
# @Desc   :

from app import db
from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.models import TaskLogFile


class TaskLogService(object):

    @staticmethod
    def delete(task_log_id: int):
        task_log: TaskLogFile = TaskLogFile.query.get(task_log_id)
        if task_log is None:
            return
        DataFileOperator(address='application').delete(file_name=task_log.alias)
        db.session.delete(task_log)
        db.session.commit()

    @staticmethod
    def get(task_log_id: int):
        task_log: TaskLogFile = ObjectAcquisition.task_log_by_id(task_log_id=task_log_id)
        task_log_message = dict()
        task_log_message['data'] = DataFileOperator(address='application').get(filename=task_log.alias)
        task_log_message['task_name'] = task_log.task.first().name

        return task_log_message

