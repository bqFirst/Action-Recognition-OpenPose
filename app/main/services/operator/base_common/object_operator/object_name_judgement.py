#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/4 9:58
# @Author : wangweimin
# @File   : object_name_judgement.py
# @Desc   : 判断是否出现重名

from sqlalchemy import and_

from app.main.basic_main.custom_error import NameRepeatedError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.base_common.project_query import get_project_data_name_list
from app.main.services.operator.base_common.appication_query import get_application_data_name_list
from app.models import Project, ProjectCatalog, Model, Database, DatabaseType, PictureLabel, ProjectProcessData, \
    ApplicationCatalog, Application, Task, CaseCatalog, Case, User


class ObjectNameRepeatedJudgement(object):

    @staticmethod
    def project_data_by_project_id(data_name: str, project_id: int):
        if data_name in get_project_data_name_list(project_id=project_id):
            raise NameRepeatedError(ErrorMsg.get_error_message(error_id=11))

    @staticmethod
    def project_by_project(project_name: str, project: Project):
        project = project.catalog.projects.filter(Project.name == project_name).first()
        if project is not None:
            raise NameRepeatedError(ErrorMsg.get_error_message(9))

    @staticmethod
    def project_by_catalog(project_name: str, catalog: ProjectCatalog):
        project = catalog.projects.filter(Project.name == project_name).first()
        if project is not None:
            raise NameRepeatedError(ErrorMsg.get_error_message(9))

    @staticmethod
    def model_by_project_id(model_name: str, user_id: int):
        model: Model = Model.query.filter(and_(Model.creator_id == user_id, Model.name == model_name)).first()
        if model is not None:
            raise NameRepeatedError(ErrorMsg.get_error_message(10))

    @staticmethod
    def database_by_type(creator_id: int, database_type: DatabaseType, database_name: str):
        database: Database = database_type.database.filter(
            and_(Database.creator_id == creator_id, Database.name == database_name)).first()
        if database is not None:
            raise NameRepeatedError(ErrorMsg.get_error_message(18))

    @staticmethod
    def picture_label(catalog_id: int, label_name: str):
        label: PictureLabel = PictureLabel.query.filter(
            and_(PictureLabel.picture_catalog_id == catalog_id, PictureLabel.name == label_name)).first()
        if label is not None:
            raise NameRepeatedError(ErrorMsg.get_error_message(24))

    @staticmethod
    def project_catalog(catalog_name: str):
        project_catalog: ProjectCatalog = ProjectCatalog.query.filter(ProjectCatalog.name == catalog_name).first()
        if project_catalog is not None:
            raise NameRepeatedError(ErrorMsg.get_error_message(1))

    @staticmethod
    def project_process_data(project_id: int, data_name: str):
        if ProjectProcessData.query.filter(and_(ProjectProcessData.project_id == project_id,
                                                ProjectProcessData.name == data_name)).first() is not None:
            raise NameRepeatedError(ErrorMsg.get_error_message(error_id=11))

    @staticmethod
    def application_data_by_application_id(data_name: str, application_id: int):
        if data_name in get_application_data_name_list(application_id=application_id):
            raise NameRepeatedError(ErrorMsg.get_error_message(error_id=11))

    @staticmethod
    def application_catalog(catalog_name: str):
        application_catalog: ApplicationCatalog = ApplicationCatalog.query.filter(
            ApplicationCatalog.name == catalog_name).first()
        if application_catalog is not None:
            raise NameRepeatedError(ErrorMsg.get_error_message(1))

    @staticmethod
    def application_by_catalog(application_name, catalog):
        application: Application = catalog.applications.filter(Application.name == application_name).first()
        if application is not None:
            raise NameRepeatedError(ErrorMsg.get_error_message(66))

    @staticmethod
    def task_by_application(task_name: str, application: Application):
        task: Task = application.tasks.filter(Task.name == task_name).first()
        if task is not None:
            raise NameRepeatedError(ErrorMsg.get_error_message(35))

    @staticmethod
    def case_catalog(catalog_name):
        case_catalog: CaseCatalog = CaseCatalog.query.filter(CaseCatalog.name == catalog_name).first()
        if case_catalog is not None:
            raise NameRepeatedError(ErrorMsg.get_error_message(1))

    @staticmethod
    def case_by_catalog(case_name, catalog: CaseCatalog):
        case: Case = catalog.cases.filter(Case.name == case_name).first()
        if case is not None:
            raise NameRepeatedError(ErrorMsg.get_error_message(62))

    @staticmethod
    def username(username):
        user: Case = User.query.filter(User.name == username).first()
        if user is not None:
            raise NameRepeatedError("用户名已存在，请重新输入")
