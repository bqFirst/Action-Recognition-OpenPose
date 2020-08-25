#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/19 0019 17:28
# @Author : wangw
# @File   : docker_image_operator_tf.py
# @Desc   :


import json
import os
import shutil
import zipfile

from docker.errors import ImageNotFound

from app import db
from app.main.basic_main.custom_error import DockerContainerNotFoundError, DockerImageNotFoundError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.docker_operator.docker_client import DockerClient
from app.main.services.operator.base_common.docker_operator.run import ModelMapFileName
from app.main.services.operator.base_common.object_operator.object_acquisition import ObjectAcquisition
from app.models import Model, ModelVersion, DockerImage
from conf.data_path import DataDirectoryPath, ModelDName, ModelSrcDName, ModelFileDName, DataDName

from app.main.services.operator.base_common.docker_operator.docker_image_operator import DockerFileNeededService
AppFile = 'run.py'
AppSklFile = 'run.py'
AppTfFile = 'run_tf.py'
DockerfileName = 'Dockerfile'
URL = 'http://127.0.0.1:{}/predict'
CurPath = os.path.abspath(os.path.dirname(__file__))
ImageName = '模型使用说明文档'


class DockerFileNeededTfService(DockerFileNeededService):

    @staticmethod
    def copy_model_data(model_id: int, docker_file_directory: str) -> ModelVersion:
        model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
        model_version: ModelVersion = model.model_version.first()

        model_file_alias: str = model_version.model_file.alias  # 模型文件名
        model_src_alias: str = model_version.model_source_code.alias  # 项目文件夹名

        # 复制模型文件
        docker_model_directory = os.path.join(docker_file_directory, DataDName, ModelDName)
        DataDirectoryPath.make_dirs(docker_model_directory)
        docker_model_file_directory = os.path.join(docker_model_directory, ModelFileDName)
        DataDirectoryPath.make_dirs(docker_model_file_directory)
        shutil.copy(os.path.join(DataDirectoryPath.get_model_file_path(), model_file_alias),
                    os.path.join(docker_model_file_directory, model_file_alias))

        # 复制项目源码文件
        docker_project_src_directory = os.path.join(docker_model_directory, ModelSrcDName)
        DataDirectoryPath.make_dirs(docker_project_src_directory)
        if os.path.isfile(model_src_alias):
            shutil.copy(os.path.join(DataDirectoryPath.get_model_src_path(), model_src_alias),
                        os.path.join(docker_project_src_directory, model_src_alias))

        else:
            shutil.copytree(os.path.join(DataDirectoryPath.get_model_src_path(), model_src_alias),
                            os.path.join(docker_project_src_directory, model_src_alias))

        return model_version

    # @classmethod
    # def create(cls, models_id: list) -> str:
    #     docker_file_alias: str = get_uuid_name()
    #     docker_directory = DataDirectoryPath.get_docker_path()
    #     docker_file_directory = os.path.join(docker_directory, docker_file_alias)
    #
    #     # 复制工程源码
    #     shutil.copytree(os.path.join(DataDirectoryPath.get_package_path(), 'app'),
    #                     os.path.join(docker_file_directory, 'app'))
    #
    #     shutil.copytree(os.path.join(DataDirectoryPath.get_package_path(), 'conf'),
    #                     os.path.join(docker_file_directory, 'conf'))
    #
    #     # 复制模型所需文件
    #     model_mapping = dict()
    #     model_type_final = 1
    #     for model_id in models_id:
    #         model_version: ModelVersion = cls.copy_model_data(model_id=model_id,
    #                                                           docker_file_directory=docker_file_directory)
    #         model_type_id = model_version.model_type_id
    #         if 1 == model_type_id:
    #             model_mapping[model_version.name] = {ModelFileDName: model_version.model_file.alias,
    #                                                  ModelSrcDName: model_version.model_source_code.alias,
    #                                                  'type': 'skl'}
    #
    #         else:
    #             model_mapping[model_version.name] = {ModelFileDName: model_version.model_file.alias,
    #                                                  ModelSrcDName: model_version.model_source_code.alias,
    #                                                  'type': 'tf'}
    #             model_type_final = model_type_id
    #
    #         # 复制flask启动文件
    #         if 1 == model_type_final:
    #             shutil.copy(os.path.join(CurPath, AppSklFile), os.path.join(docker_file_directory, AppFile))
    #         elif 2 == model_type_final:
    #             shutil.copy(os.path.join(CurPath, AppTfFile), os.path.join(docker_file_directory, AppFile))
    #
    #         # 复制Dockerfile
    #         if 2 == model_type_final:
    #             shutil.copy(os.path.join(CurPath, 'tf_docker_file', DockerfileName),
    #                         os.path.join(docker_file_directory, DockerfileName))
    #         else:
    #             shutil.copy(os.path.join(CurPath,  'skl_docker_file', DockerfileName),
    #                         os.path.join(docker_file_directory, DockerfileName))
    #
    #         # 保存模型文件与模型名称映射关系
    #         with open(os.path.join(docker_file_directory, ModelMapFileName), 'w') as f:
    #             json.dump(model_mapping, f)
    #
    #         return docker_file_directory






