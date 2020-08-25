#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/4 15:58
# @Author : wangweimin
# @File   : project_catalog_operator.py
# @Desc   :


from app import db
from app.main.services.operator.base_common.data_base_operator.data_transform import datetime2timestamp
from app.main.basic_main.custom_error import UserOperatorError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectExistJudgement, \
    ObjectNameRepeatedJudgement
from app.models import ProjectCatalog, Project, Model, ModelVersion


class ProjectCatalogService(object):

    @classmethod
    def tree(cls, catalog_id: int) -> list:
        result = []
        for project in Project.query.filter(Project.catalog_id == catalog_id).order_by(Project.name).all():
            project_msg = dict()
            project_msg['type'] = 'project'
            project_msg['name'] = project.name
            project_msg['project_id'] = project.id
            result.append(project_msg)
        project_catalogs: list = ProjectCatalog.query.filter(ProjectCatalog.pid == catalog_id).order_by(
            ProjectCatalog.name).all()
        for project_catalog in project_catalogs:
            catalog_menu = dict()
            catalog_menu['name'] = project_catalog.name
            catalog_menu['type'] = 'catalog'
            catalog_menu['catalog_id'] = project_catalog.id
            catalog_menu['child'] = cls.tree(catalog_id=project_catalog.id)
            catalog_menu['create_time'] = datetime2timestamp(project_catalog.create_time)
            if '默认目录' == catalog_menu['name']:
                result.insert(0, catalog_menu)
            else:
                result.append(catalog_menu)
        return result

    @classmethod
    def create(cls, catalog_pid: int, catalog_name: str, user_id: int) -> int:
        ObjectExistJudgement.project_catalog_pig(catalog_pid=catalog_pid)
        ObjectNameRepeatedJudgement.project_catalog(catalog_name=catalog_name)  # 不允许重名
        project_catalog: ProjectCatalog = ProjectCatalog(name=catalog_name, pid=catalog_pid, creator_id=user_id)
        db.session.add(project_catalog)
        db.session.commit()
        return project_catalog.id

    @classmethod
    def rename(cls, catalog_name: str, catalog_id: int):
        project_catalog: ProjectCatalog = ObjectAcquisition.project_catalog_by_id(catalog_id=catalog_id)
        if project_catalog.name != catalog_name:
            ObjectNameRepeatedJudgement.project_catalog(catalog_name=catalog_name)  # 不允许重名
            project_catalog.name = catalog_name
            db.session.commit()

    @classmethod
    def project_info(cls, catalog_id: int) -> list:
        result = []
        if 0 == catalog_id:
            projects: list = Project.query.all()
        else:
            project_catalog: ProjectCatalog = ObjectAcquisition.project_catalog_by_id(catalog_id=catalog_id)
            projects = project_catalog.projects.all()
        for project in projects:
            project_msg = dict()
            project_msg['creator'] = project.creator.name
            project_msg['project_id'] = project.id
            project_msg['create_time'] = project.create_time
            project_msg['project_name'] = project.name
            result.append(project_msg)
        return result

    @classmethod
    def delete(cls, catalog_id: int):
        project_catalog: ProjectCatalog = ObjectAcquisition.project_catalog_by_id(catalog_id=catalog_id)

        if ProjectCatalog.query.filter(ProjectCatalog.pid == catalog_id).first() or Project.query.filter(
                Project.catalog_id == catalog_id).first():  # 判断该目录下是否有工程或目录
            raise UserOperatorError(ErrorMsg.get_error_message(2))
        else:
            db.session.delete(project_catalog)
            db.session.commit()
            return

    @classmethod
    def get(cls, catalog_id: int):
        project_catalog: ProjectCatalog = ObjectAcquisition.project_catalog_by_id(catalog_id=catalog_id)
        return {'catalog_id': catalog_id, 'catalog_name': project_catalog.name}

    @classmethod
    def model_tree(cls, catalog_id: int, user_id: int, models_id: list) -> list:
        if catalog_id:
            catalogs: list = [ObjectAcquisition.project_catalog_by_id(catalog_id=catalog_id)]
        else:
            catalogs: list = ProjectCatalog.query.filter(ProjectCatalog.creator_id == user_id).all()
        result = []
        for catalog in catalogs:
            projects = catalog.projects.all()
            project_info = []
            for project in projects:
                models = project.models.filter(Model.id.notin_(models_id)).all()
                model_info = []
                for model in models:
                    model_version: ModelVersion = model.model_version.first()
                    if model_version.status_id in [1, 3]:
                        continue
                    model_msg = dict()
                    model_msg['model_name'] = model.name
                    model_msg['model_id'] = model.id
                    model_msg['type'] = 'model'
                    model_msg['create_time'] = datetime2timestamp(model.create_time)
                    model_info.append(model_msg)
                if model_info:
                    project_msg = dict()
                    project_msg['child'] = model_info
                    project_msg['project_name'] = project.name
                    project_msg['project_id'] = project.id
                    project_msg['create_time'] = datetime2timestamp(project.create_time)
                    project_msg['type'] = 'project'
                    project_info.append(project_msg)
            if project_info:
                catalog_msg = dict()
                catalog_msg['catalog_name'] = catalog.name
                catalog_msg['catalog_id'] = catalog.id
                catalog_msg['create_time'] = datetime2timestamp(catalog.create_time)
                catalog_msg['type'] = 'catalog'
                catalog_msg['child'] = project_info
                result.append(catalog_msg)
        return result
