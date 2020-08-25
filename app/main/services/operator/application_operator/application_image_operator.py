#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/3/6 17:09
# @Author : wangweimin
# @File   : application_image_operator.py
# @Desc   :

import os
import shutil

from app import db
from app.models import DockerImageFile

from conf.data_path import DataDirectoryPath


class ApplicationImageService(object):

    @staticmethod
    def create() -> DockerImageFile:
        application_image: DockerImageFile = DockerImageFile()
        db.session.add(application_image)
        db.session.commit()
        return application_image

    @staticmethod
    def __delete_alias(alias: str):
        if alias:
            image_file: str = os.path.join(DataDirectoryPath.get_docker_image_path(), alias)
            if os.path.exists(image_file):
                os.remove(image_file)

    @classmethod
    def delete(cls, application_image: DockerImageFile):
        alias: str = application_image.alias
        cls.__delete_alias(alias=alias)
        db.session.delete(application_image)
        db.session.commit()

    @classmethod
    def reset(cls, application_image: DockerImageFile):
        """应用在增删模型后需要重置状态"""
        alias: str = application_image.alias
        cls.__delete_alias(alias=alias)
        application_image.status_id = 1
        db.session.commit()
