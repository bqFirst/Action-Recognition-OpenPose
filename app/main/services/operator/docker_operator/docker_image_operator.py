#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/1/6 15:04
# @Author : wangweimin
# @File   : docker_image_operator.py
# @Desc   :

import os

from app import db
from app.main.basic_main.custom_error import UserOperatorError
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.main.services.operator.base_common.docker_base_operator.docker_actual_image_operator import DockerImageService
from app.models import BaseDockerImage
from conf.data_path import DataDirectoryPath


class DockerBaseImageService(object):

    @classmethod
    def base_image_info(cls) -> list:
        result = []
        for base_image in BaseDockerImage.query.all():
            base_image_info = dict()
            base_image_info['docker_image_id'] = base_image.id
            base_image_info['docker_image_name'] = base_image.name
            result.append(base_image_info)
        return result

    @classmethod
    def package(cls, base_image: BaseDockerImage) -> str:
        if 2 == base_image.status_id:
            raise UserOperatorError("打包中，请等待")
        alias: str = get_uuid_name('.zip')
        base_image.status_id = 2
        db.session.commit()
        try:
            DockerImageService.save(image_file=os.path.join(DataDirectoryPath.get_docker_image_path(), alias),
                                    tags=base_image.tags)
            base_image.alias = alias
            base_image.status_id = 3
            db.session.commit()
            return alias
        except Exception:
            base_image.status_id = 1
            db.session.commit()
            raise

    @classmethod
    def download(cls, docker_image_id: int) -> tuple:
        base_image: BaseDockerImage = ObjectAcquisition.base_image(docker_image_id=docker_image_id)
        alias: str = base_image.alias
        if not isinstance(alias, str) or not os.path.exists(  # 未打包或者打包文件不存在
                os.path.join(DataDirectoryPath.get_docker_image_path(), alias)):
            alias: str = cls.package(base_image=base_image)
        return DataDirectoryPath.get_model_package_path(), alias, base_image.name + '.zip'
