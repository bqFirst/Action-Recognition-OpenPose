#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/29 10:24
# @Author : wangwei
# @File   : application_picture_catalog_operator.py
# @Desc   :

from app import db
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectNameRepeatedJudgement
from app.main.basic_main.custom_error import RequestIdError, UserOperatorError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.picture_operator.picture_operator import PictureService
from app.main.services.operator.picture_operator.picture_catalog_ioperator import PictureCatalogService, \
    PictureCatalogPictureService
from app.models import PictureCatalog, Application, Task


class AppPictureCatalogService(PictureCatalogService):

    @classmethod
    def create(
            cls,
            application_id: int,
            catalog_name: str,
            pictures: list,
            creator_id: int) -> int:
        ObjectNameRepeatedJudgement.application_data_by_application_id(
            data_name=catalog_name, application_id=application_id)
        application: Application = ObjectAcquisition.application_by_id(
            application_id=application_id)
        pictures = cls.check_pictures(pictures=pictures)
        picture_catalog: PictureCatalog = PictureCatalog(
            name=catalog_name, creator_id=creator_id)
        db.session.add(picture_catalog)
        application.picture_catalogs.append(picture_catalog)
        db.session.commit()

        PictureCatalogPictureService.save(
            catalog_id=picture_catalog.id,
            creator_id=creator_id,
            pictures=pictures)
        cls.record_cale(catalog_id=picture_catalog.id)
        return picture_catalog.id

    @classmethod
    def delete(cls, catalog_id: int, is_forced=False) -> bool:
        picture_catalog: PictureCatalog = ObjectAcquisition.picture_catalog(
            catalog_id=catalog_id, ascription='application')
        if not is_forced:
            task_list = picture_catalog.tasks.with_entities(Task.name).all()
            if len(task_list) > 0:
                task_name_list = [x[0] for x in task_list]
                raise UserOperatorError(
                    ErrorMsg.get_error_message(31).format(
                        ','.join(task_name_list)))

        for picture in picture_catalog.pictures:
            PictureService.delete(picture=picture)

        db.session.delete(picture_catalog)
        db.session.commit()
        return True

    @classmethod
    def rename(
            cls,
            catalog_id: int,
            catalog_name: str,
            application_id: int = None):
        picture_catalog: PictureCatalog = ObjectAcquisition.picture_catalog(
            catalog_id=catalog_id, ascription='application')
        if application_id is not None and application_id != picture_catalog.applications.first().id:
            raise RequestIdError(ErrorMsg.get_error_message(27))
        else:
            application_id = picture_catalog.applications.first().id
        if picture_catalog.name == catalog_name:
            return
        ObjectNameRepeatedJudgement.application_data_by_application_id(
            application_id=application_id, data_name=catalog_name)
        picture_catalog.name = catalog_name
        db.session.commit()
