#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/6 10:55
# @Author : wangweimin
# @File   : application_catalog_operator.py
# @Desc   :


from app import db
from app.main.basic_main.custom_error import UserOperatorError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.base_common.data_base_operator.data_transform import datetime2timestamp
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectExistJudgement, \
    ObjectNameRepeatedJudgement
from app.models import Application, ApplicationCatalog, ApplicationStatus, DockerImageStatus


class ApplicationCatalogService(object):

    @classmethod
    def tree(cls, catalog_id: int) -> list:
        result = []
        for application in Application.query.filter(Application.catalog_id == catalog_id).order_by(
                Application.create_time.desc()).all():
            application_msg = dict()
            application_msg['type'] = 'application'
            application_msg['name'] = application.name
            application_msg['application_id'] = application.id
            application_msg['create_time'] = datetime2timestamp(application.create_time)
            result.append(application_msg)
        application_catalogs: list = ApplicationCatalog.query.filter(ApplicationCatalog.pid == catalog_id).order_by(
            ApplicationCatalog.name).all()
        for application_catalog in application_catalogs:
            catalog_menu = dict()
            catalog_menu['name'] = application_catalog.name
            catalog_menu['type'] = 'catalog'
            catalog_menu['catalog_id'] = application_catalog.id
            catalog_menu['child'] = cls.tree(catalog_id=application_catalog.id)
            if '默认目录' == catalog_menu['name']:
                result.insert(0, catalog_menu)
            else:
                result.append(catalog_menu)
        return result

    @classmethod
    def create(cls, catalog_pid: int, catalog_name: str, user_id: int) -> int:
        ObjectExistJudgement.application_catalog_pid(catalog_pid=catalog_pid)
        ObjectNameRepeatedJudgement.application_catalog(catalog_name=catalog_name)
        application_catalog: ApplicationCatalog = ApplicationCatalog(name=catalog_name, pid=catalog_pid,
                                                                     creator_id=user_id)
        db.session.add(application_catalog)
        db.session.commit()
        return application_catalog.id

    @classmethod
    def delete(cls, catalog_id: int):
        application_catalog: ApplicationCatalog = ObjectAcquisition.application_catalog_by_id(catalog_id=catalog_id)

        # 判断该目录下是否有应用或目录
        if ApplicationCatalog.query.filter(
                ApplicationCatalog.pid == catalog_id).first() or application_catalog.applications.first() is not None:
            raise UserOperatorError(ErrorMsg.get_error_message(2))
        db.session.delete(application_catalog)
        db.session.commit()
        return

    @classmethod
    def rename(cls, catalog_id: int, catalog_name: str):
        application_catalog: ApplicationCatalog = ObjectAcquisition.application_catalog_by_id(catalog_id=catalog_id)
        if application_catalog.name != catalog_name:
            ObjectNameRepeatedJudgement.application_catalog(catalog_name=catalog_name)  # 不允许重名
            application_catalog.name = catalog_name
            db.session.commit()

    @classmethod
    def application_info(cls, catalog_id: int, user_id: int):
        result = []
        if 0 == catalog_id:
            applications: list = Application.query.filter(Application.creator_id == user_id).all()
        else:
            application_catalog: ApplicationCatalog = ObjectAcquisition.application_catalog_by_id(catalog_id=catalog_id)
            applications = application_catalog.applications.all()
        for application in applications:
            application_msg = dict()
            application_msg['creator'] = application.creator.name
            application_msg['application_id'] = application.id
            application_msg['create_time'] = application.create_time
            application_msg['application_name'] = application.name
            status: ApplicationStatus = application.status
            application_msg['status_name'] = status.name
            application_msg['status_id'] = status.id
            image_status: DockerImageStatus = application.application_image.image_status
            application_msg['image_status_id'] = image_status.id
            application_msg['image_status_name'] = image_status.image_status
            result.append(application_msg)
        return result
