#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/29 16:43
# @Author : wangweimin
# @File   : project_edit_window_operator.py
# @Desc   :

from app import db
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.models import Project, ProjectEditWindow


class ProjectEditWindowService(object):

    @staticmethod
    def __get_project_by_id(project_id: int) -> Project:
        project: Project = Project.query.get(project_id)
        if project is None:
            raise ValueError('Error project id')
        return project

    @classmethod
    def get_window_by_id(cls, project_id: int) -> ProjectEditWindow:
        project: Project = cls.__get_project_by_id(project_id=project_id)
        window: ProjectEditWindow = project.edit_window.first()
        if window is None:
            return cls.create(project_id=project_id)
        else:
            return window

    @classmethod
    def create(cls, project_id: int) -> ProjectEditWindow:
        project: Project = cls.__get_project_by_id(project_id=project_id)
        alias: str = get_uuid_name(suffix='json')
        DataFileOperator(address='project').put(
            data={'model_name': '', 'model_id': 0, 'description': '', 'src': '', 'data_format': ''},
            file_name=alias)
        try:
            window: ProjectEditWindow = ProjectEditWindow(project=project, alias=alias)
            db.session.add(window)
            db.session.commit()
            return window
        except Exception:
            DataFileOperator(address='project').delete(file_name=alias)
            raise

    @classmethod
    def delete(cls, project_id: int):
        project: Project = cls.__get_project_by_id(project_id=project_id)
        window: ProjectEditWindow = project.edit_window.first()
        DataFileOperator(address='project').delete(file_name=window.alias)
        db.session.delete(window)
        db.session.commit()

    @classmethod
    def get(cls, project_id: int) -> dict:
        window: ProjectEditWindow = cls.get_window_by_id(project_id=project_id)
        return DataFileOperator(address='project').get(filename=window.alias)

    @classmethod
    def save(cls, project_id: int, model_name: str, description: str, src: str, data_format: str):
        window: ProjectEditWindow = cls.get_window_by_id(project_id=project_id)
        DataFileOperator(address='project').put(
            data={'model_name': model_name, 'description': description, 'src': src, 'data_format': str(data_format)},
            file_name=window.alias)
