#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/19 15:05
# @Author : wangweimin
# @File   : project_process_data_operator.py
# @Desc   :

import pandas as pd

from app import db, socketio
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.data_base_operator.data_cale import get_data_link_record
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectNameRepeatedJudgement
from app.main.services.operator.base_common.websocket_operator.websocket_operator import WebSocketService
from app.main.services.operator.project_operator.project_path import get_project_id_by_path
from app.models import ProjectProcessData
from conf.data_path import DataDirectoryPath


class ProjectProcessService(object):

    @classmethod
    def delete(cls, project_id: int, process_data_id: int):
        process_data: ProjectProcessData = ObjectAcquisition.project_process_data(project_id=project_id,
                                                                                  process_data_id=process_data_id)
        DataFileOperator(address='project').delete(process_data.alias)
        db.session.delete(process_data)
        db.session.commit()
        return

    @classmethod
    def rename(cls, project_id: int, process_data_id: int, data_name: str):
        process_data: ProjectProcessData = ObjectAcquisition.project_process_data(project_id=project_id,
                                                                                  process_data_id=process_data_id)
        if process_data.name == data_name:
            return
        ObjectNameRepeatedJudgement.project_process_data(project_id=project_id, data_name=data_name)
        process_data.name = data_name
        db.session.commit()
        return

    @classmethod
    def download(cls, project_id: int, process_data_id: int) -> tuple:
        process_data: ProjectProcessData = ObjectAcquisition.project_process_data(project_id=project_id,
                                                                                  process_data_id=process_data_id)
        filename: str = process_data.name
        suffix: str = process_data.type
        if '.' not in filename:
            filename = filename + '.' + suffix
        elif suffix != filename.split('.')[-1]:
            filename = filename + '.' + suffix
        return DataDirectoryPath.get_project_path(), process_data.alias, filename

    @classmethod
    def get(cls, project_id: int, process_data_id: int, page: int, limit: int):
        process_data: ProjectProcessData = ObjectAcquisition.project_process_data(project_id=project_id,
                                                                                  process_data_id=process_data_id)
        data = DataFileOperator(address='project').get(filename=process_data.alias,
                                                       paging={'start': page * limit, 'nrows': limit})
        return data, get_data_link_record(process_data)

    @classmethod
    def create(cls, data: pd.DataFrame, filename: str, project_path: str, **kwargs) -> int:
        project_id = get_project_id_by_path(project_path=project_path)
        ObjectNameRepeatedJudgement.project_process_data(project_id=project_id, data_name=filename)

        data_alias = get_uuid_name(suffix='csv')
        status = DataFileOperator(address='project').put(data=data, file_name=data_alias, **kwargs)
        if status:
            process_data: ProjectProcessData = ProjectProcessData(name=filename, alias=data_alias, data_type_id=1,
                                                                  project_id=project_id, record=data.shape[0])
            db.session.add(process_data)
            db.session.commit()
            WebSocketService.emit(event='refresh', address='process', project_id=project_id)
            return process_data.id


class ProjectProcessesService(object):

    @classmethod
    def info(cls, project_id: int):
        project = ObjectAcquisition.project_by_id(project_id=project_id)
        result = []
        data_processes = project.process_data.all()
        for data_process in data_processes:
            data_process_info = dict()
            data_process_info['data_name'] = data_process.name
            data_process_info['process_data_id'] = data_process.id
            data_process_info['data_type'] = data_process.data_type.data_type
            data_process_info['create_time'] = data_process.create_time
            # Todo
            # 创建者名称之后添加
            data_process_info['creator'] = 'm'
            result.append(data_process_info)
        return result
