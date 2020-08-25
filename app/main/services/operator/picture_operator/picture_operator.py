#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/7 15:37
# @Author : wangweimin
# @File   : picture_operator.py
# @Desc   :

import os
from PIL import Image
from sqlalchemy import and_

from app import db

from app.main.basic_main.custom_error import FileNotExistError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.picture_operator.picture_config import PictureUrlCompose, ThumbnailHigh, ThumbnailWide
from app.models import Picture, Thumbnail
from conf.data_path import DataDirectoryPath


class PictureService(object):

    @classmethod
    def save(cls, picture, address='original', is_thumbnail=True) -> dict:
        """
        使用多线程保存，因此数据入库需要回到主线程操作
        """
        img = Image.open(picture)
        picture_name: str = picture.filename
        suffix = picture_name.rsplit('.', 1)[-1] or 'jpg'
        suffix = suffix.lower()
        picture_alias: str = get_uuid_name(suffix=suffix)
        DataFileOperator(address=address).put(data=img, file_name=picture_alias)
        # 保存缩略图
        thumbnail_alias: str = ''
        if is_thumbnail:
            thumbnail_alias: str = ThumbnailService.save(img=img, suffix=suffix)
        return {'picture_alias': picture_alias, 'picture_name': picture_name, 'thumbnail_alias': thumbnail_alias}

    @classmethod
    def warehousing(cls, catalog_id: int, picture_name: str, picture_alias: str, thumbnail_alias: str) -> Picture:
        picture: Picture = Picture.query.filter(
            and_(Picture.name == picture_name, Picture.picture_catalog_id == catalog_id)).first()
        if picture is not None:
            cls.delete(picture=picture)

        thumbnail: Thumbnail = ThumbnailService.warehousing(thumbnail_alias=thumbnail_alias)
        picture_: Picture = Picture(name=picture_name, alias=picture_alias, picture_catalog_id=catalog_id,
                                    thumbnail=thumbnail)
        db.session.add(picture_)
        db.session.commit()
        return picture_

    @classmethod
    def delete(cls, picture: Picture):
        DataFileOperator(address='original').delete(file_name=picture.alias)
        thumbnail: Thumbnail = picture.thumbnail
        db.session.delete(picture)
        db.session.commit()
        ThumbnailService.delete(thumbnail=thumbnail)

    @classmethod
    def get(cls, picture_id: int) -> dict:
        picture: Picture = ObjectAcquisition.picture_by_id(picture_id=picture_id)
        return {'picture_name': picture.name, 'picture_id': picture.id, 'picture_label': picture.label,
                'original_url': PictureUrlCompose.original(alias=picture.alias)}

    @classmethod
    def get_size(cls, picture: Picture) -> int:
        size = picture.size
        if size is None:
            try:
                size = os.path.getsize(os.path.join(DataDirectoryPath.get_original_picture_path(), picture.alias))
            except FileNotFoundError:
                raise FileNotExistError(ErrorMsg.get_error_message(23))
            picture.size = size
            db.session.commit()
        return size


class ThumbnailService(object):

    @classmethod
    def save(cls, img, suffix: str, img_w: int = ThumbnailWide, img_h: int = ThumbnailHigh) -> str:
        img.thumbnail((img_w, img_h))
        thumbnail_alias: str = get_uuid_name(suffix=suffix)
        DataFileOperator(address='thumbnail').put(data=img, file_name=thumbnail_alias)
        return thumbnail_alias

    @classmethod
    def warehousing(cls, thumbnail_alias: str) -> Thumbnail:
        thumbnail: Thumbnail = Thumbnail(alias=thumbnail_alias)
        db.session.add(thumbnail)
        db.session.commit()
        return thumbnail

    @classmethod
    def delete(cls, thumbnail: Thumbnail):
        DataFileOperator(address='thumbnail').delete(file_name=thumbnail.alias)
        db.session.delete(thumbnail)
        db.session.commit()
