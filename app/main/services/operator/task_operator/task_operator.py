#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/7 17:35
# @Author : wangweimin
# @File   : task_operator.py
# @Desc   :

import datetime

from app import db
from app.main.basic_main.custom_error import UserOperatorError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.data_base_operator.data_operator import DataService
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectNameRepeatedJudgement
from app.main.services.operator.task_operator.task_execute_operator import TaskExecuteService
from app.main.services.operator.task_operator.task_log_operator import TaskLogService
from app.main.services.operator.task_operator.task_result_operator import TaskResultService
from app.main.services.operator.task_operator.time_operator import TimeService
from app.models import Application, Task, TaskResultFile, TaskLogFile, Model


class TaskService(object):

    @classmethod
    def create(cls, data_link_id: int, task_name: str, application_id: int, description: str, data_type: str,
               user_id: int, model_id: int) -> int:
        application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
        if 1 != application.status_id:
            raise UserOperatorError(ErrorMsg.get_error_message(38))
        model: Model = ObjectAcquisition.model_by_application(model_id=model_id, application=application)
        task_type_id, data_link = DataService.get(data_link_id=data_link_id, data_type=data_type)
        if task_type_id == 2:
            raise UserOperatorError('暂无图片预测功能')
        ObjectNameRepeatedJudgement.task_by_application(task_name=task_name, application=application)
        start_time = datetime.datetime.now()
        log_file: str = get_uuid_name(suffix='txt')
        task_log: TaskLogFile = TaskLogFile(alias=log_file)
        db.session.add(task_log)
        alias: str = get_uuid_name(suffix='csv')
        task_result: TaskResultFile = TaskResultFile(alias=alias, name=task_name + "_结果数据.csv")
        db.session.add(task_result)
        db.session.commit()
        task: Task = Task(description=description, name=task_name, application_id=application_id, creator_id=user_id,
                          task_type_id=task_type_id, model_id=model.id, log_file_id=task_log.id,
                          result_file_id=task_result.id)
        db.session.add(task)
        db.session.commit()
        data_link.tasks.append(task)
        db.session.commit()
        log_message = '[{}] 离线任务-{}，开始运行'.format(TimeService.to_str(start_time), task_name)
        DataFileOperator(address='application').put(data=log_message, file_name=log_file)
        # Todo
        # 后台执行
        TaskExecuteService.execute(task=task, data_link=data_link, start_time=start_time)
        return task.id

    @classmethod
    def delete(cls, task_id: int):
        task: Task = ObjectAcquisition.task_by_id(task_id=task_id)
        task_status_id = task.status_id
        if 1 == task_status_id:
            raise UserOperatorError(ErrorMsg.get_error_message(36))
        elif 2 == task_status_id:
            raise UserOperatorError(ErrorMsg.get_error_message(37))
        TaskResultService.delete(task.result_file_id)
        TaskLogService.delete(task.log_file_id)
        db.session.delete(task)
        db.session.commit()

    @classmethod
    def restart(cls, task_id):
        task: Task = ObjectAcquisition.task_by_id(task_id=task_id)
        if task.status_id not in [3, 4, 5]:
            raise UserOperatorError(ErrorMsg.get_error_message(55))
        task.run_time = datetime.datetime.utcnow()
        db.session.commit()
        start_time = datetime.datetime.now()
        log_message = '[{}] 离线任务-{}，开始运行'.format(TimeService.to_str(start_time), task.name)
        DataFileOperator(address='application').add(data=log_message, file_name=task.log.alias)
        # Todo
        # 后台执行
        TaskExecuteService.execute(task=task, data_link=task.predicted_data_link, start_time=start_time)
