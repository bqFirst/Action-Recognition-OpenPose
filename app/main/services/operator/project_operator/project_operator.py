#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/7 11:04
# @Author : wangweimin
# @File   : project_operator.py
# @Desc   :

from app import db
from app.main.basic_main.custom_error import UserOperatorError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectNameRepeatedJudgement
from app.main.services.operator.project_operator.project_edit_window_operator import ProjectEditWindowService
from app.models import Project, ProjectCatalog, DataSourceDataLink, Model, ProjectProcessData, PictureCatalog, \
    DatabaseData


class ProjectService(object):

    @classmethod
    def create(cls, catalog_id: int, user_id: int, description: str, project_name: str, data_links_id: list):
        catalog: ProjectCatalog = ObjectAcquisition.project_catalog_by_id(catalog_id=catalog_id)
        ObjectNameRepeatedJudgement.project_by_catalog(project_name=project_name, catalog=catalog)
        project = Project(name=project_name, description=description, creator_id=user_id, modifier_id=user_id,
                          catalog_id=catalog_id)
        db.session.add(project)
        db.session.commit()
        for data_link_id in data_links_id:
            data_link: DataSourceDataLink = DataSourceDataLink.query.get(data_link_id)
            if data_link is None:
                continue
            project.data_links.append(data_link)
        db.session.commit()
        ProjectEditWindowService.create(project_id=project.id)
        return project.id

    @classmethod
    def rename(cls, project_id: int, project_name: str):
        project: Project = ObjectAcquisition.project_by_id(project_id=project_id)
        if project.name == project_name:
            return
        ObjectNameRepeatedJudgement.project_by_project(project_name=project_name, project=project)
        project.name = project_name
        db.session.commit()
        return

    @classmethod
    def delete(cls, project_id: int) -> None:
        project: Project = ObjectAcquisition.project_by_id(project_id=project_id)
        model: Model = project.models.first()
        if model is not None:
            raise UserOperatorError(ErrorMsg.get_error_message(14))
        process_data: ProjectProcessData = project.process_data.first()
        if process_data is not None:
            raise UserOperatorError(ErrorMsg.get_error_message(13))
        data_link: DataSourceDataLink = project.data_links.first()
        if data_link is not None:
            raise UserOperatorError(ErrorMsg.get_error_message(12))
        picture_catalog: PictureCatalog = project.picture_catalogs.first()
        if picture_catalog is not None:
            raise UserOperatorError(ErrorMsg.get_error_message(12))
        database_data: DatabaseData = project.database_data.first()
        if database_data is not None:
            raise UserOperatorError(ErrorMsg.get_error_message(12))
        ProjectEditWindowService.delete(project_id=project_id)
        db.session.delete(project)
        db.session.commit()
        return

    @classmethod
    def get(cls, project_id: int) -> dict:
        project: Project = ObjectAcquisition.project_by_id(project_id=project_id)
        return {'project_id': project_id, 'project_name': project.name, 'create_time': project.create_time,
                'creator': project.creator.name, 'catalog_name': project.catalog.name,
                'description': project.description}
