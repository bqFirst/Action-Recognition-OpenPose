#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/4 11:16
# @Author : wangweimin
# @File   : task_execute_operator.py
# @Desc   :

import datetime
import pandas as pd
import requests

from app import db
from app.main.basic_main.custom_error import DockerContainerPredictError, UserOperatorError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.websocket_operator.websocket_operator import WebSocketService
from app.main.services.operator.task_operator.time_operator import TimeService
from app.main.services.operator.task_operator.task_config import Url
from app.models import Application, Task, TaskResultFile, TaskLogFile


class TaskExecuteService(object):

    @staticmethod
    def get_url(task: Task) -> str:
        application: Application = task.application
        model_name: str = task.model_name
        port: int = application.container.port
        url = Url.format(port, model_name)
        return url

    @classmethod
    def data2container(cls, data: pd.DataFrame, task: Task) -> pd.DataFrame:
        url = cls.get_url(task=task)
        respond = requests.post(url, data={'data': data.to_json(orient='records')})
        result: dict = respond.json()
        code = result.get('code')
        if code:
            raise DockerContainerPredictError(result.get('message').get('Error'))
        result: pd.DataFrame = pd.DataFrame(result['data'])
        if result.shape[0] == data.shape[0]:
            result = data.join(result)
        return result

    @classmethod
    def request_with_data(cls, data: pd.DataFrame, task: Task):
        result = cls.data2container(data=data, task=task)
        task_result: TaskResultFile = task.result
        if task_result is None:
            alias: str = get_uuid_name(suffix='csv')
            task_result: TaskResultFile = TaskResultFile(alias=alias, name=task.name + "_结果数据.csv")
            db.session.add(task_result)
            db.session.commit()
            task.result_file_id = task_result.id
            db.session.commit()
        alias = task_result.alias
        DataFileOperator(address='application').put(data=result, file_name=alias)

    @classmethod
    def request_with_picture(cls, data, task: Task):
        raise UserOperatorError('暂无图片预测功能')
        pass

    @classmethod
    def execute(cls, task: Task, data_link, start_time: datetime.datetime):
        task_log: TaskLogFile = task.log
        log_message = ''
        # noinspection PyBroadException
        try:
            task_type_id = task.task_type_id
            if 2 == task_type_id:  # 图片
                data = None
                cls.request_with_picture(data=data, task=task)
            else:
                if task_type_id in [1, 4, ]:  # 文件数据
                    data = DataFileOperator(address='data_source').get(filename=data_link.alias)
                else:  # 数据库数据
                    data = DataFileOperator(address='database').get(filename=data_link.alias)
                cls.request_with_data(data=data, task=task)

            task.status_id = 4
            db.session.commit()
            now = datetime.datetime.now()
            time_delta = (now - start_time).total_seconds()
            log_message = '[{}] 离线任务-{}，运行成功，耗时 {} 毫秒。生成结果数据《{}_结果数据.csv》'.format(TimeService.to_str(now), task.name,
                                                                                  TimeService.to_millisecond(
                                                                                      time_delta), task.name)
            DataFileOperator(address='application').add(data=log_message, file_name=task_log.alias)
        except DockerContainerPredictError as e:
            log_message = cls.__execute__error(start_time=start_time, task=task,
                                               error_message=str(e), log_alias=task_log.alias)
        except Exception:
            log_message = cls.__execute__error(start_time=start_time, task=task,
                                               error_message=ErrorMsg.get_error_message(30), log_alias=task_log.alias)
        finally:
            WebSocketService.emit(event='log', address='task', log_id=task_log.id, data=log_message)

    @staticmethod
    def __execute__error(start_time: datetime.datetime, task: Task, error_message: str, log_alias: str) -> str:
        task.status_id = 5
        db.session.commit()
        now = datetime.datetime.now()
        time_delta = (now - start_time).total_seconds()
        log_message = '[{}] 离线任务-{}，运行失败，耗时 {} 毫秒。\n{}'.format(TimeService.to_str(now), task.name,
                                                               TimeService.to_millisecond(second=time_delta),
                                                               error_message)
        DataFileOperator(address='application').add(data=log_message, file_name=log_alias)
        return log_message
