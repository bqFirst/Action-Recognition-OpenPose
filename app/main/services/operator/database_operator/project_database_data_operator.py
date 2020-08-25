#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/6 10:33
# @Author : wangweimin
# @File   : project_database_data_operator.py
# @Desc   :


from app import db
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.basic_main.custom_error import RequestIdError
from app.main.services.operator.base_common.data_base_operator.data_overview_operator import DataOverviewService
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectNameRepeatedJudgement, \
    ObjectExistJudgement
from app.main.services.operator.database_operator.database_idata_operator import DatabaseDataService
from app.models import DatabaseData, Project


class ProDatabaseDataService(DatabaseDataService):

    @classmethod
    def create(cls, data_name: str, database_id: int, project_id: int, sql: str, creator_id: int) -> int:
        project: Project = ObjectAcquisition.project_by_id(project_id=project_id)
        ObjectNameRepeatedJudgement.project_data_by_project_id(project_id=project_id, data_name=data_name)
        data = cls.select_data(database_id=database_id, creator_id=creator_id, sql=sql)
        alias: str = get_uuid_name(suffix='db.csv')
        DataFileOperator(address='database').put(data=data, file_name=alias)
        database_data: DatabaseData = DatabaseData(name=data_name, alias=alias, sql=sql, record=data.shape[0],
                                                   database_id=database_id)
        db.session.add(database_data)
        db.session.commit()
        project.database_data.append(database_data)
        db.session.commit()
        return database_data.id

    @classmethod
    def edit(cls, data_name: str, database_id: int, project_id: int, sql: str, creator_id: int,
             data_link_id: int) -> int:
        database_data: DatabaseData = ObjectAcquisition.database_data(database_data_id=data_link_id,
                                                                      ascription='project')
        ObjectExistJudgement.database_id(database_id=database_id)
        ObjectExistJudgement.project_id(project_id=project_id)
        if data_name != database_data.name:
            ObjectNameRepeatedJudgement.project_data_by_project_id(project_id=project_id, data_name=data_name)
        data = cls.select_data(database_id=database_id, creator_id=creator_id, sql=sql)
        DataOverviewService.delete(data_link=database_data)
        alias = database_data.alias
        dfo = DataFileOperator(address='database')
        dfo.delete(file_name=alias)
        dfo.put(data=data, file_name=alias)
        database_data.name = data_name
        database_data.sql = sql
        database_data.record = data.shape[0]
        database_data.database_id = database_id
        database_data.is_used = 0
        # database_data.create_time = datetime.utcnow()
        db.session.commit()
        return database_data.id

    @classmethod
    def rename(cls, data_link_id: int, data_name: str, project_id: int = None):
        database_data: DatabaseData = ObjectAcquisition.database_data(database_data_id=data_link_id,
                                                                      ascription='project')
        if project_id is not None and project_id != database_data.project.id:
            raise RequestIdError(ErrorMsg.get_error_message(27))
        else:
            project_id = database_data.project.id
        ObjectNameRepeatedJudgement.project_data_by_project_id(project_id=project_id, data_name=data_name)
        database_data.name = data_name
        db.session.commit()

    @classmethod
    def delete(cls, data_link_id: int, is_forced=False) -> bool:
        database_data: DatabaseData = ObjectAcquisition.database_data(database_data_id=data_link_id,
                                                                      ascription='project')
        if database_data.is_used and not is_forced:
            return False
        DataOverviewService.delete(data_link=database_data)
        alias: str = database_data.alias
        DataFileOperator(address='database').delete(file_name=alias)
        db.session.delete(database_data)
        db.session.commit()
        return True
