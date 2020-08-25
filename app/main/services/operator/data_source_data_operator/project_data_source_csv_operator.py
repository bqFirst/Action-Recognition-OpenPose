#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/6 17:28
# @Author : wangweimin
# @File   : project_data_source_csv_operator.py
# @Desc   :

from app import db
from app.models import DataSourceDataLink, Project, DataType
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.basic_main.custom_error import UserOperatorError, RequestIdError
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.base_common.data_base_operator.data_overview_operator import DataOverviewService
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectExistJudgement, \
    ObjectNameRepeatedJudgement
from app.main.services.operator.data_source_data_operator.data_source_icsv_operator import DsCsvService


class ProDsCsvService(DsCsvService):

    @classmethod
    def upload(cls, f, data_name: str, catalog_id: int, user_id: int, data_type: str, project_id: int) -> int:
        project: Project = ObjectAcquisition.project_by_id(project_id=project_id)
        ObjectExistJudgement.ds_catalog_id(catalog_id=catalog_id)
        ObjectNameRepeatedJudgement.project_data_by_project_id(data_name=data_name, project_id=project_id)
        data_type: DataType = ObjectAcquisition.data_type_by_name(data_type=data_type)
        cls.check_csv(f=f)
        data = cls.parsing(f)
        alias = get_uuid_name(suffix='csv')
        DataFileOperator(address='data_source').put(data=data, file_name=alias)
        data_link = DataSourceDataLink(name=data_name, alias=alias, data_type=data_type, creator_id=user_id,
                                       catalog_id=catalog_id, record=data.shape[0])
        db.session.add(data_link)
        db.session.commit()
        data_link.projects.append(project)
        db.session.commit()
        return data_link.id

    @classmethod
    def rename(cls, data_link_id: int, catalog_id: int, new_name: str, project_id: int=None):
        data_link: DataSourceDataLink = ObjectAcquisition.ds_data_link(data_link_id=data_link_id, ascription='project')
        if project_id is not None and project_id != data_link.projects.first().id:
            raise RequestIdError(ErrorMsg.get_error_message(27))
        else:
            project_id = data_link.projects.first().id
        if data_link.name == new_name:
            return
        if new_name is not None:
            ObjectNameRepeatedJudgement.project_data_by_project_id(data_name=new_name, project_id=project_id)
            data_link.name = new_name
        if catalog_id is not None:
            data_link.catalog_id = catalog_id
        db.session.commit()

    @classmethod
    def delete(cls, data_link_id: int, is_forced=False) -> bool:
        data_link: DataSourceDataLink = ObjectAcquisition.ds_data_link(data_link_id=data_link_id, ascription='project')
        if data_link.is_used and not is_forced:
            return False
        projects: list = data_link.projects.all()
        if projects is None:
            pass
        else:
            for project in projects:
                data_link.projects.remove(project)
            db.session.commit()
        alias = data_link.alias
        DataFileOperator(address='data_source').delete(file_name=alias)
        DataOverviewService.delete(data_link=data_link)
        db.session.delete(data_link)
        db.session.commit()
        return True
