#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/2 17:25
# @Author : wangweimin
# @File   : docker_actual_container_operator.py
# @Desc   :

import time
import json
import os
import shutil

from app import db
from app.main.basic_main.custom_error import DockerContainerNotFoundError, UserOperatorError
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.operator.base_common.docker_base_operator.docker_client import DockerClient, WaitContainerTime
from app.main.services.operator.base_common.docker_base_operator.docker_actual_image_operator import DockerImageService
from app.main.services.operator.base_common.object_operator.object_acquisition import ObjectAcquisition
from app.models import Model, ModelVersion, DockerContainer, DockerImage, DockerPort
from conf.data_path import DataDirectoryPath, ModelSrcDName, ModelFileDName

AppFile = 'run.py'
AppSklFile = 'run.py'
CurPath = os.path.abspath(os.path.dirname(__file__))
ModelMapFileName = 'model_mapping.json'


class SklModelDataRecordService(object):
    """
    制作模型信息dict
    model_mapping = {
            'model_name1': {'file': 'xxxxxxxxxxx1.pkl', 'src': 'xxxxxxxxxxx1.py', 'type': 1},  # 1代表skl模型
            'model_name2': {'file': 'xxxxxxxxxxx2.pkl', 'src': 'xxxxxxxxxxx2.py', 'type': 1},
    }
    """
    @classmethod
    def create(cls, models_id: list) -> str:
        docker_file_alias: str = get_uuid_name()
        docker_directory = DataDirectoryPath.get_docker_path()
        docker_file_directory = os.path.join(docker_directory, docker_file_alias)
        try:
            os.mkdir(docker_file_directory)

            # 创建模型信息
            model_mapping = dict()
            for model_id in models_id:
                model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
                model_version: ModelVersion = model.model_version.first()
                model_type_id = model_version.model_type_id
                if 1 == model_type_id:
                    model_mapping[model_version.name] = {ModelFileDName: model_version.model_file.alias,
                                                         ModelSrcDName: model_version.model_source_code.alias,
                                                         'type': 'skl'}
                else:
                    raise UserOperatorError("tensorflow暂不支持与sklearn一起打包")

            # 复制flask启动文件
            shutil.copy(os.path.join(CurPath, 'skl_docker_file', AppSklFile), os.path.join(docker_file_directory, AppFile))

            # 保存模型文件与模型名称映射关系
            with open(os.path.join(docker_file_directory, ModelMapFileName), 'w') as f:
                json.dump(model_mapping, f)

            return docker_file_alias
        except Exception:
            if os.path.exists(docker_file_directory):
                shutil.rmtree(docker_file_directory, True)
            raise


class DockerContainerService(object):

    @staticmethod
    def stop(short_id: str):
        container = DockerClient.get_container(short_id=short_id)
        container.stop()
        time.sleep(WaitContainerTime)

    @staticmethod
    def start(short_id: str):
        container = DockerClient.get_container(short_id=short_id)
        container.start()
        time.sleep(WaitContainerTime)

    @staticmethod
    def remove(short_id: str):
        """
        $ docker rm -f short_id
        """
        container = DockerClient.get_container(short_id=short_id)
        container.remove(force=True)

    @staticmethod
    def status(short_id: str) -> bool:
        container = DockerClient.get_container(short_id=short_id)
        status = container.status
        if 'running' == status:
            return True
        else:
            return False

    @classmethod
    def delete_old(cls, container: DockerContainer, keep_port=False):
        container_short_id = container.short_id
        try:
            cls.stop(short_id=container_short_id)
            cls.remove(short_id=container_short_id)
        except DockerContainerNotFoundError:
            pass
        image: DockerImage = container.image
        DockerImageService.delete(image=image)
        if not keep_port:
            server_port: DockerPort = container.docker_port
            db.session.delete(server_port)
            db.session.commit()
        db.session.delete(container)
        db.session.commit()

    @classmethod
    def delete(cls, container: DockerContainer, keep_port=False):
        container_short_id = container.short_id
        try:
            cls.stop(short_id=container_short_id)
            cls.remove(short_id=container_short_id)
        except DockerContainerNotFoundError:
            pass
        alias = container.alias
        if alias:
            docker_file_directory = os.path.join(DataDirectoryPath.get_docker_path(), alias)
            if os.path.exists(docker_file_directory):
                shutil.rmtree(docker_file_directory, True)
        if not keep_port:
            server_port: DockerPort = container.docker_port
            db.session.delete(server_port)
            db.session.commit()
        db.session.delete(container)
        db.session.commit()
