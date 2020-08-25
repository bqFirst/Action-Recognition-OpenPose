#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/7 10:27
# @Author : wangweimin
# @File   : project_picture_catalog_operator.py
# @Desc   :

from app import db
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectNameRepeatedJudgement
from app.main.basic_main.custom_error import RequestIdError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.picture_operator.picture_label_operator import PictureLabelService
from app.main.services.operator.picture_operator.picture_operator import PictureService
from app.main.services.operator.picture_operator.picture_catalog_ioperator import PictureCatalogService, \
    PictureCatalogPictureService

from app.models import PictureCatalog, Project, PictureLabel, Picture


class ProPictureCatalogService(PictureCatalogService):

    @classmethod
    def create(cls, project_id: int, catalog_name: str, pictures: list, label_name: str, creator_id: int) -> int:
        ObjectNameRepeatedJudgement.project_data_by_project_id(data_name=catalog_name, project_id=project_id)
        project: Project = ObjectAcquisition.project_by_id(project_id=project_id)
        pictures = cls.check_pictures(pictures=pictures)
        picture_catalog: PictureCatalog = PictureCatalog(name=catalog_name, creator_id=creator_id)
        db.session.add(picture_catalog)
        picture_catalog.projects.append(project)
        db.session.commit()
        picture_label: PictureLabel = None
        if label_name:
            picture_label: PictureLabel = PictureLabelService.create_and_return(catalog_id=picture_catalog.id,
                                                                                label_name=label_name)
        PictureCatalogPictureService.save(catalog_id=picture_catalog.id, creator_id=creator_id,
                                          picture_label=picture_label, pictures=pictures)
        cls.record_cale(catalog_id=picture_catalog.id)
        return picture_catalog.id

    @classmethod
    def delete(cls, catalog_id: int, is_forced: bool) -> bool:
        picture_catalog: PictureCatalog = ObjectAcquisition.picture_catalog(catalog_id=catalog_id, ascription='project')
        pictures_query = picture_catalog.pictures
        if pictures_query.filter(Picture.is_used == 1).first() is not None and not is_forced:
            return False
        # 标签删除，依次删除图片，缩略图
        for picture in picture_catalog.pictures:
            PictureService.delete(picture=picture)
        picture_catalog.labels.delete()
        db.session.delete(picture_catalog)
        db.session.commit()
        return True

    @classmethod
    def rename(cls, catalog_id: int, catalog_name: str, project_id: int = None):
        picture_catalog: PictureCatalog = ObjectAcquisition.picture_catalog(catalog_id=catalog_id, ascription='project')
        if project_id is not None and project_id != picture_catalog.projects.first().id:
            raise RequestIdError(ErrorMsg.get_error_message(27))
        else:
            project_id = picture_catalog.projects.first().id
        if picture_catalog.name == catalog_name:
            return
        ObjectNameRepeatedJudgement.project_data_by_project_id(project_id=project_id,
                                                               data_name=catalog_name)
        picture_catalog.name = catalog_name
        db.session.commit()
