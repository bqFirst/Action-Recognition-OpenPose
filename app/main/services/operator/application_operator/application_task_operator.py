#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/6 16:23
# @Author : wangwei
# @File   : application_task_operator.py
# @Desc   : 

from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.models import Application, TaskStatus, TaskResultFile, Task


class ApplicationTaskService(object):

    @classmethod
    def get(cls, application_id: int, status_id: int):
        application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
        tasks: list = application.tasks.order_by(Task.run_time.desc()).all()
        result = []
        for task in tasks:
            task_status: TaskStatus = task.task_status
            task_status_id = task_status.id
            task_msg = dict()
            if 0 == status_id or task_status_id == status_id:
                task_msg['task_id'] = task.id
                task_msg['task_name'] = task.name
                task_msg['status_id'] = task.status_id
                task_msg['status_name'] = task_status.name
                task_msg['run_time'] = task.run_time
                predicted_data_link = task.predicted_data_link
                task_msg['predicted_data_name'] = predicted_data_link.name
                task_msg['predicted_data_id'] = predicted_data_link.id
                task_msg['data_type'] = predicted_data_link.type
                task_msg['creator'] = task.creator.name
                if 4 == task_status_id:
                    task_result: TaskResultFile = task.result
                    task_msg['result_data_name'] = task_result.name
                    task_msg['result_data_id'] = task_result.id
                else:
                    task_msg['result_data_id'] = task_status_id
                    task_msg['result_data_name'] = ''
                task_msg['task_log_id'] = task.log_file_id
                result.append(task_msg)
        return result
