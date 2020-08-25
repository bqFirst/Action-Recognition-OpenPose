#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/29 10:17
# @Author : wangwei
# @File   : application_data_source_csv_operator.py
# @Desc   :

from app import db
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.basic_main.custom_error import UserOperatorError, RequestIdError
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.base_common.data_base_operator.data_overview_operator import DataOverviewService
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectExistJudgement, \
    ObjectNameRepeatedJudgement
from app.main.services.operator.data_source_data_operator.data_source_icsv_operator import DsCsvService
from app.models import DataSourceDataLink, Application, DataType, Task


class AppDsCsvService(DsCsvService):

    @classmethod
    def upload(cls, f, data_name: str, catalog_id: int, user_id: int, data_type: str, application_id: int) -> int:

        application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
        ObjectExistJudgement.ds_catalog_id(catalog_id=catalog_id)
        ObjectNameRepeatedJudgement.application_data_by_application_id(data_name=data_name,
                                                                       application_id=application_id)

        data_type: DataType = ObjectAcquisition.data_type_by_name(data_type=data_type)

        cls.check_csv(f=f)
        data = cls.parsing(f)

        alias = get_uuid_name(suffix='csv')
        DataFileOperator(address='data_source').put(data=data, file_name=alias)
        data_link = DataSourceDataLink(name=data_name, alias=alias, data_type=data_type, creator_id=user_id,
                                       catalog_id=catalog_id, record=data.shape[0])
        db.session.add(data_link)
        db.session.commit()
        data_link.applications.append(application)
        db.session.commit()
        return data_link.id

    @classmethod
    def rename(cls, data_link_id: int, catalog_id: int, new_name: str, application_id: int = None):

        data_link: DataSourceDataLink = ObjectAcquisition.ds_data_link(data_link_id=data_link_id,
                                                                       ascription='application')

        if application_id is not None and application_id != data_link.applications.first().id:
            raise RequestIdError(ErrorMsg.get_error_message(27))
        else:
            application_id = data_link.applications.first().id

        if data_link.name == new_name:
            return

        if new_name is not None:
            ObjectNameRepeatedJudgement.application_data_by_application_id(data_name=new_name,
                                                                           application_id=application_id)
            data_link.name = new_name

        if catalog_id is not None:
            data_link.catalog_id = catalog_id
        db.session.commit()

    @classmethod
    def delete(cls, data_link_id: int, is_forced=False) -> bool:
        data_link: DataSourceDataLink = ObjectAcquisition.ds_data_link(data_link_id=data_link_id,
                                                                       ascription='application')

        if not is_forced:
            task_list = data_link.tasks.with_entities(Task.name).all()
            if len(task_list) > 0:
                task_name_list = [x[0] for x in task_list]
                raise UserOperatorError(ErrorMsg.get_error_message(31).format(','.join(task_name_list)))
        applications: list = data_link.applications.all()

        for application in applications:
            data_link.applications.remove(application)
        db.session.commit()

        alias = data_link.alias

        DataFileOperator(address='data_source').delete(file_name=alias)
        DataOverviewService.delete(data_link=data_link)
        db.session.delete(data_link)
        db.session.commit()
        return True
