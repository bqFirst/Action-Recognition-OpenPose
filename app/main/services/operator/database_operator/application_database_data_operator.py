#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/29 10:22
# @Author : wangwei
# @File   : application_database_data_operator.py
# @Desc   :

from app import db
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.basic_main.custom_error import RequestIdError, UserOperatorError
from app.main.services.operator.base_common.data_base_operator.data_overview_operator import DataOverviewService
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectNameRepeatedJudgement, \
    ObjectExistJudgement
from app.models import DatabaseData, Application, Task
from app.main.services.operator.database_operator.database_idata_operator import DatabaseDataService


class AppDatabaseDataService(DatabaseDataService):

    @classmethod
    def create(
            cls,
            data_name: str,
            database_id: int,
            application_id: int,
            sql: str,
            creator_id: int) -> int:
        application: Application = ObjectAcquisition.application_by_id(
            application_id=application_id)
        ObjectNameRepeatedJudgement.application_data_by_application_id(
            application_id=application_id, data_name=data_name)
        data = cls.select_data(
            database_id=database_id,
            creator_id=creator_id,
            sql=sql)
        alias: str = get_uuid_name(suffix='db.csv')
        DataFileOperator(address='database').put(data=data, file_name=alias)
        database_data: DatabaseData = DatabaseData(
            name=data_name,
            alias=alias,
            sql=sql,
            record=data.shape[0],
            database_id=database_id)
        db.session.add(database_data)
        db.session.commit()
        application.database_data.append(database_data)
        db.session.commit()
        return database_data.id

    @classmethod
    def edit(
            cls,
            data_name: str,
            database_id: int,
            application_id: int,
            sql: str,
            creator_id: int,
            data_link_id: int) -> int:
        database_data: DatabaseData = ObjectAcquisition.database_data(
            database_data_id=data_link_id, ascription='application')
        ObjectExistJudgement.database_id(database_id=database_id)
        ObjectExistJudgement.application_id(application_id=application_id)
        if data_name != database_data.name:
            ObjectNameRepeatedJudgement.application_data_by_application_id(
                application_id=application_id, data_name=data_name)
        data = cls.select_data(
            database_id=database_id,
            creator_id=creator_id,
            sql=sql)
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
        db.session.commit()
        return database_data.id

    @classmethod
    def rename(
            cls,
            data_link_id: int,
            data_name: str,
            application_id: int = None):
        database_data: DatabaseData = ObjectAcquisition.database_data(
            database_data_id=data_link_id, ascription='application')
        if application_id is not None and application_id != database_data.application.id:
            raise RequestIdError(ErrorMsg.get_error_message(27))
        else:
            application_id = database_data.application.id

        ObjectNameRepeatedJudgement.application_data_by_application_id(
            application_id=application_id, data_name=data_name)
        database_data.name = data_name
        db.session.commit()

    @classmethod
    def delete(cls, data_link_id: int, is_forced=False):
        database_data: DatabaseData = ObjectAcquisition.database_data(
            database_data_id=data_link_id, ascription='application')

        if not is_forced:

            task_list = database_data.tasks.with_entities(Task.name).all()
            if len(task_list) > 0:
                task_name_list = [x[0] for x in task_list]
                raise UserOperatorError(
                    ErrorMsg.get_error_message(31).format(
                        ','.join(task_name_list)))

        DataOverviewService.delete(data_link=database_data)
        alias: str = database_data.alias
        DataFileOperator(address='database').delete(file_name=alias)
        db.session.delete(database_data)
        db.session.commit()
        return True
