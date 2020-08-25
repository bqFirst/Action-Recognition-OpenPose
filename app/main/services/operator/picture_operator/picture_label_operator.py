#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/8 9:49
# @Author : wangweimin
# @File   : picture_label_operator.py
# @Desc   :

from app import db
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectNameRepeatedJudgement, \
    ObjectExistJudgement
from app.models import PictureLabel, Picture, PictureCatalog


class PictureLabelService(object):

    @staticmethod
    def __get_picture_label(catalog_id: int, label_name: str) -> PictureLabel:
        return PictureLabel.query.filter(PictureLabel.name == label_name,
                                         PictureLabel.picture_catalog_id == catalog_id).first()

    @classmethod
    def create_and_return(cls, catalog_id: int, label_name: str) -> PictureLabel:
        picture_label = cls.__get_picture_label(catalog_id=catalog_id, label_name=label_name)
        if picture_label is None:
            picture_label: PictureLabel = PictureLabel(name=label_name, picture_catalog_id=catalog_id)
            db.session.add(picture_label)
            db.session.commit()
        return picture_label

    @classmethod
    def create(cls, catalog_id: int, label_name: str, pictures_id: list) -> int:
        ObjectExistJudgement.picture_catalog_id(catalog_id=catalog_id)
        label: PictureLabel = cls.create_and_return(catalog_id=catalog_id, label_name=label_name)
        PictureLabelPictureService.add(catalog_id=catalog_id, label_id=label.id, pictures_id=pictures_id)
        return label.id

    @classmethod
    def delete(cls, label_id: int, catalog_id: int):
        label: PictureLabel = ObjectAcquisition.picture_label(catalog_id=catalog_id, label_id=label_id)
        db.session.delete(label)
        db.session.commit()

    @classmethod
    def rename(cls, label_id: int, catalog_id: int, label_name: str):
        label: PictureLabel = ObjectAcquisition.picture_label(catalog_id=catalog_id, label_id=label_id)
        if label.name == label_name:
            return
        ObjectNameRepeatedJudgement.picture_label(catalog_id=catalog_id, label_name=label_name)
        label.name = label_name
        db.session.commit()


class PictureLabelPictureService(object):

    @classmethod
    def delete(cls, catalog_id: int, label_id: int, pictures_id: list):
        label: PictureLabel = ObjectAcquisition.picture_label(catalog_id=catalog_id, label_id=label_id)
        pictures = label.pictures.filter(Picture.id.in_(pictures_id)).all()
        for picture in pictures:
            label.pictures.remove(picture)
        db.session.commit()

    @classmethod
    def add(cls, catalog_id: int, label_id: int, pictures_id: list):
        label: PictureLabel = ObjectAcquisition.picture_label(catalog_id=catalog_id, label_id=label_id)
        picture_catalog: PictureCatalog = ObjectAcquisition.picture_catalog(catalog_id=catalog_id)
        pictures = picture_catalog.pictures.filter(Picture.id.in_(pictures_id)).all()
        for picture in pictures:
            # 一张图片只有一个标签
            if 0 != picture.label_num:
                continue
            label.pictures.append(picture)
        db.session.commit()
