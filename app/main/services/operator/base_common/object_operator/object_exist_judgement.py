#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/4 9:53
# @Author : wangweimin
# @File   : object_exist_judgement.py
# @Desc   :

from sqlalchemy import and_

from app.main.basic_main.custom_error import RequestIdError, RequestValueError
from app.main.basic_main.error_message import ErrorMsg
from app.models import ProjectCatalog, Project, DataSourceCatalog, Database, PictureCatalog, ApplicationCatalog, \
    Application, Model, CaseCatalog


class ObjectExistJudgement(object):

    @staticmethod
    def project_catalog_pig(catalog_pid: int):
        if 0 != catalog_pid and ProjectCatalog.query.get(catalog_pid) is None:
            raise RequestIdError('Error catalog pid')

    @staticmethod
    def project_id(project_id: int):
        if Project.query.get(project_id) is None:
            raise RequestIdError('Error project id')

    @staticmethod
    def ds_catalog_id(catalog_id: int):
        if DataSourceCatalog.query.get(catalog_id) is None:
            raise RequestIdError('Error catalog id')

    @staticmethod
    def database_id(database_id: int):
        if Database.query.get(database_id) is None:
            raise RequestIdError('Error catalog id')

    @staticmethod
    def picture_catalog_id(catalog_id: int):
        if PictureCatalog.query.get(catalog_id) is None:
            raise RequestIdError('Error catalog id')

    @staticmethod
    def application_catalog_pid(catalog_pid: int):
        if 0 != catalog_pid and ApplicationCatalog.query.get(catalog_pid) is None:
            raise RequestIdError('Error catalog pid')

    @staticmethod
    def application_id(application_id: int):
        if Application.query.get(application_id) is None:
            raise RequestIdError('Error application id')

    @staticmethod
    def models_id(models_id):
        models: list = Model.query.filter(Model.id.in_(models_id)).all()
        if len(models_id) != len(models):
            raise RequestIdError('Error model id')

    @staticmethod
    def model_name(model_name: str, user_id: int):
        model: Model = Model.query.filter(and_(Model.creator_id == user_id, Model.name == model_name)).first()
        if model is not None:
            raise RequestValueError(ErrorMsg.get_error_message(56))

    @staticmethod
    def case_catalog_pid(catalog_pid):
        if 0 != catalog_pid and CaseCatalog.query.get(catalog_pid) is None:
            raise RequestIdError('Error catalog pid')
