#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/3 16:47
# @Author : wangweimin
# @File   : picture_catalog_ioperator.py
# @Desc   :

from concurrent.futures import ThreadPoolExecutor, wait
from sqlalchemy import not_

from app import db
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectNameRepeatedJudgement, \
    ObjectExistJudgement
from app.main.basic_main.custom_error import RequestIdError, UserOperatorError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.picture_operator.picture_label_operator import PictureLabelService
from app.main.services.operator.picture_operator.picture_operator import PictureService
from app.main.services.operator.picture_operator.picture_config import PictureUrlCompose, PictureSaveThreadPoolNum

from app.models import PictureCatalog, PictureLabel, Picture


class PictureCatalogService(object):

    @staticmethod
    def allowed_file(picture_name: str) -> bool:
        return '.' in picture_name and picture_name.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png']

    @classmethod
    def check_pictures(cls, pictures: list) -> list:
        allowed_pictures = [picture for picture in pictures if cls.allowed_file(picture_name=picture.filename)]
        if len(allowed_pictures) == 0:
            raise UserOperatorError(ErrorMsg.get_error_message(68))
        return allowed_pictures

    @staticmethod
    def record_cale(catalog_id: int):
        picture_catalog: PictureCatalog = ObjectAcquisition.picture_catalog(catalog_id=catalog_id)
        record: int = picture_catalog.pictures.count()
        if record != picture_catalog.record:
            picture_catalog.record = record
            db.session.commit()

    @classmethod
    def labels(cls, catalog_id: int) -> dict:
        picture_catalog: PictureCatalog = ObjectAcquisition.picture_catalog(catalog_id=catalog_id)
        result = []
        for label in picture_catalog.labels.all():
            label_info = dict()
            label_info['label_name'] = label.name
            label_info['label_id'] = label.id
            result.append(label_info)
        return {'catalog_name': picture_catalog.name, 'data': result}

    @classmethod
    def picture_names(cls, catalog_id: int) -> list:
        picture_catalog: PictureCatalog = ObjectAcquisition.picture_catalog(catalog_id=catalog_id)
        picture_names_result = picture_catalog.pictures.with_entities(Picture.name).all()
        result: list = [x[0] for x in picture_names_result]
        return result

    @staticmethod
    def __get_picture_id_with_label(catalog_id: int) -> list:
        picture_catalog: PictureCatalog = ObjectAcquisition.picture_catalog(catalog_id=catalog_id)
        labels: list = picture_catalog.labels.all()
        picture_id = []
        for label in labels:
            picture_id.extend([x[0] for x in label.pictures.with_entities(Picture.id).all()])
        return list(set(picture_id))

    @classmethod
    def pictures_info(cls, catalog_id: int, label_id: int, limit: int, page: int) -> dict:
        picture_catalog: PictureCatalog = ObjectAcquisition.picture_catalog(catalog_id=catalog_id)
        result = {'catalog_name': picture_catalog.name}
        if label_id == 0:
            picture_query = picture_catalog.pictures
        elif -1 == label_id:
            picture_query = picture_catalog.pictures.filter(
                not_(Picture.id.in_(cls.__get_picture_id_with_label(catalog_id=catalog_id))))
        else:
            label = ObjectAcquisition.picture_label(catalog_id=catalog_id, label_id=label_id)
            picture_query = label.pictures
        total: int = picture_query.count()
        data_result = []
        if limit * (page - 1) > total:
            pass
        else:
            paginate = picture_query.paginate(page, limit)
            for picture in paginate.items:
                picture_info = dict()
                picture_info['picture_name'] = picture.name
                picture_info['picture_id'] = picture.id
                picture_info['thumbnail_url'] = PictureUrlCompose.thumbnail(picture.thumbnail.alias)
                picture_info['original_url'] = PictureUrlCompose.original(picture.alias)
                picture_info['size'] = PictureService.get_size(picture)
                data_result.append(picture_info)
        result.update(data=data_result)
        return result

    @classmethod
    def rename(cls, catalog_id: int, catalog_name: str, project_id: int=None):
        picture_catalog: PictureCatalog = ObjectAcquisition.picture_catalog(catalog_id=catalog_id)
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

    @classmethod
    def add_newly(cls, catalog_id: int, pictures: list, label_name: str, creator_id: int):
        ObjectExistJudgement.picture_catalog_id(catalog_id=catalog_id)
        cls.check_pictures(pictures=pictures)
        picture_label: PictureLabel = None
        if label_name:
            picture_label: PictureLabel = PictureLabelService.create_and_return(catalog_id=catalog_id,
                                                                                label_name=label_name)
        PictureCatalogPictureService.save(catalog_id=catalog_id, pictures=pictures, picture_label=picture_label, creator_id=creator_id)
        PictureCatalogService.record_cale(catalog_id=catalog_id)


class PictureCatalogPictureService(object):

    @staticmethod
    def __allowed_file(picture_name: str) -> bool:
        return '.' in picture_name and picture_name.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png']

    @classmethod
    def save(cls, catalog_id: int, pictures: list, creator_id: int, picture_label: PictureLabel = None):
        # ObjectExistJudgement.picture_catalog_id(catalog_id=catalog_id)

        pool = ThreadPoolExecutor(max_workers=PictureSaveThreadPoolNum)
        future_list = []
        allowed_pictures = [picture for picture in pictures if cls.__allowed_file(picture_name=picture.filename)]
        if len(allowed_pictures) == 0:
            raise UserOperatorError(ErrorMsg.get_error_message(68))
        for picture in allowed_pictures:
            future_list.append(pool.submit(PictureService.save, picture=picture))
        wait(future_list)

        for future in future_list:
            result: dict = future.result()
            thumbnail_alias: str = result.get('thumbnail_alias')
            picture_name: str = result.get('picture_name')
            picture_alias: str = result.get('picture_alias')
            picture_: Picture = PictureService.warehousing(catalog_id=catalog_id, thumbnail_alias=thumbnail_alias,
                                                           picture_name=picture_name, picture_alias=picture_alias)
            if picture_label is not None:
                picture_label.pictures.append(picture_)
        if picture_label is not None:
            db.session.commit()


class PictureCatalogLabelService(object):

    @classmethod
    def info(cls, catalog_id: int, creator_id: int) -> dict:
        picture_catalog: PictureCatalog = ObjectAcquisition.picture_catalog(catalog_id=catalog_id)
        picture_labels = []
        picture_label_count = 0
        for picture_label in picture_catalog.labels:
            picture_label_info = dict()
            picture_label_info['label_name'] = picture_label.name
            picture_label_info['label_id'] = picture_label.id
            picture_label_info['pictures_count'] = picture_label.pictures.count()
            picture_label_count += picture_label_info['pictures_count']
            picture_labels.append(picture_label_info)
        return {'non_label_count': picture_catalog.pictures.count() - picture_label_count, 'label': picture_labels}
