#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/2 16:14
# @Author : wangweimin
# @File   : docker_actual_image_operator.py
# @Desc   :

import json
import os
import shutil
import zipfile

from docker.errors import ImageNotFound

from app import db
from app.main.basic_main.custom_error import DockerContainerNotFoundError, ParameterError
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.docker_base_operator.docker_client import DockerClient
from app.main.services.operator.base_common.object_operator.object_acquisition import ObjectAcquisition
from app.models import Model, ModelVersion, DockerImage
from conf.data_path import DataDirectoryPath, ModelDName, ModelSrcDName, ModelFileDName, DataDName

AppFile = 'run.py'
AppImageSklFile = 'image_run.py'
AppTfFile = 'run_tf.py'
DockerfileName = 'Dockerfile'
CurPath = os.path.abspath(os.path.dirname(__file__))
ImageName = '模型使用说明文档'
ModelMapFileName = 'model_mapping.json'


class ModelDataPackageService(object):

    @classmethod
    def unused_single_model(cls, model_id: int):

        docker_file_alias: str = get_uuid_name()
        docker_directory = DataDirectoryPath.get_docker_path()
        docker_file_directory = os.path.join(docker_directory, docker_file_alias)
        DataDirectoryPath.make_dirs(docker_file_directory)

        # model_file = os.path.join(DataDirectoryPath.get_model_file_path(), model_file_alias)  # 模型文件全路径
        # model_src = os.path.join(DataDirectoryPath.get_model_src_path(), model_src_alias)  # 模型源码全路径
        model_version: ModelVersion = cls.copy_model_data(model_id=model_id,
                                                          model_package_directory=docker_file_directory)
        model_src_alias: str = model_version.model_source_code.alias  # 模型源码名
        model_type_id: int = model_version.model_type_id

        # 复制flask启动文件
        # shutil.copy(os.path.join(CurPath, AppFile), os.path.join(docker_file_directory, AppFile))
        if 1 == model_type_id:
            shutil.copy(os.path.join(CurPath, AppImageSklFile), os.path.join(docker_file_directory, AppFile))
        elif 2 == model_type_id:
            shutil.copy(os.path.join(CurPath, AppTfFile), os.path.join(docker_file_directory, AppFile))
        else:
            raise ValueError('Model type is undefined')

        # 复制Dockerfile
        if 2 == model_type_id:
            shutil.copy(os.path.join(CurPath, 'tf_docker_file', DockerfileName),
                        os.path.join(docker_file_directory, DockerfileName))
        else:
            src = DataFileOperator(address='src').get(filename=model_src_alias)
            if 'dask' in src:
                shutil.copy(os.path.join(CurPath, 'dask_docker_file', DockerfileName),
                            os.path.join(docker_file_directory, DockerfileName))
            else:
                shutil.copy(os.path.join(CurPath, 'skl_docker_file', DockerfileName),
                            os.path.join(docker_file_directory, DockerfileName))

        # 复制工程源码
        shutil.copytree(os.path.join(DataDirectoryPath.get_package_path(), 'app'),
                        os.path.join(docker_file_directory, 'app'))
        shutil.copytree(os.path.join(DataDirectoryPath.get_package_path(), 'conf'),
                        os.path.join(docker_file_directory, 'conf'))
        with open(os.path.join(docker_file_directory, 'model_mapping.json'), 'w') as f:
            json.dump({model_version.model_file.alias: model_version.name}, f)

        return docker_file_directory

    @staticmethod
    def copy_model_data(model_id: int, model_package_directory: str) -> ModelVersion:
        model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
        model_version: ModelVersion = model.model_version.first()

        model_file_alias: str = model_version.model_file.alias  # 模型文件名
        model_src_alias: str = model_version.model_source_code.alias  # 模型源码名

        # 复制模型文件
        docker_model_directory = os.path.join(model_package_directory, DataDName, ModelDName)
        DataDirectoryPath.make_dirs(docker_model_directory)
        docker_model_file_directory = os.path.join(docker_model_directory, ModelFileDName)
        DataDirectoryPath.make_dirs(docker_model_file_directory)
        shutil.copy(os.path.join(DataDirectoryPath.get_model_file_path(), model_file_alias),
                    os.path.join(docker_model_file_directory, model_file_alias))

        # 复制模型源码文件
        docker_model_src_directory = os.path.join(docker_model_directory, ModelSrcDName)
        DataDirectoryPath.make_dirs(docker_model_src_directory)
        shutil.copy(os.path.join(DataDirectoryPath.get_model_src_path(), model_src_alias),
                    os.path.join(docker_model_src_directory, model_src_alias))

        return model_version

    @classmethod
    def create(cls, models_id: list) -> str:
        docker_file_alias: str = get_uuid_name()
        docker_directory = DataDirectoryPath.get_docker_path()
        docker_file_directory = os.path.join(docker_directory, docker_file_alias)
        os.mkdir(docker_file_directory)

        # 复制工程源码
        shutil.copytree(os.path.join(DataDirectoryPath.get_package_path(), 'app'),
                        os.path.join(docker_file_directory, 'app'))
        shutil.copytree(os.path.join(DataDirectoryPath.get_package_path(), 'conf'),
                        os.path.join(docker_file_directory, 'conf'))

        # 复制模型所需文件
        model_mapping = dict()
        model_type_final = 1
        for model_id in models_id:
            model_version: ModelVersion = cls.copy_model_data(model_id=model_id,
                                                              model_package_directory=docker_file_directory)
            model_type_id = model_version.model_type_id
            if 1 == model_type_id:
                model_mapping[model_version.name] = {ModelFileDName: model_version.model_file.alias,
                                                     ModelSrcDName: model_version.model_source_code.alias,
                                                     'type': 'skl'}
            else:
                model_mapping[model_version.name] = {ModelFileDName: model_version.model_file.alias,
                                                     ModelSrcDName: model_version.model_source_code.alias,
                                                     'type': 'tf'}
                model_type_final = model_type_id

        # 复制flask启动文件
        if 1 == model_type_final:
            shutil.copy(os.path.join(CurPath, 'skl_docker_file', AppImageSklFile),
                        os.path.join(docker_file_directory, AppFile))
        elif 2 == model_type_final:
            shutil.copy(os.path.join(CurPath, 'tf_docker_file', AppTfFile),
                        os.path.join(docker_file_directory, AppFile))

        # 复制Dockerfile
        if 2 == model_type_final:
            shutil.copy(os.path.join(CurPath, 'tf_docker_file', DockerfileName),
                        os.path.join(docker_file_directory, DockerfileName))
        else:
            shutil.copy(os.path.join(CurPath, 'skl_docker_file', DockerfileName),
                        os.path.join(docker_file_directory, DockerfileName))

        # 保存模型文件与模型名称映射关系
        with open(os.path.join(docker_file_directory, DataDName, ModelMapFileName), 'w') as f:
            json.dump(model_mapping, f)

        return docker_file_directory

    @classmethod
    def model_package(cls, model_id: int) -> tuple:
        model_package_alias: str = get_uuid_name()
        model_package_directory = DataDirectoryPath.get_model_package_path()
        model_package_directory = os.path.join(model_package_directory, model_package_alias)
        os.mkdir(model_package_directory)

        # 复制模型所需文件
        model_mapping = dict()
        model_type_final = 1
        model_version: ModelVersion = cls.copy_model_data(model_id=model_id,
                                                          model_package_directory=model_package_directory)
        model_type_id = model_version.model_type_id
        if 1 == model_type_id:
            model_mapping[model_version.name] = {ModelFileDName: model_version.model_file.alias,
                                                 ModelSrcDName: model_version.model_source_code.alias,
                                                 'type': 'skl'}
        else:
            model_mapping[model_version.name] = {ModelFileDName: model_version.model_file.alias,
                                                 ModelSrcDName: model_version.model_source_code.alias,
                                                 'type': 'tf'}
            model_type_final = model_type_id

        # 保存模型文件与模型名称映射关系
        with open(os.path.join(model_package_directory, DataDName, ModelMapFileName), 'w') as f:
            json.dump(model_mapping, f)

        return model_package_directory, model_type_final

    @staticmethod
    def zip(original_path: str, destination_path: str, model_description: str = '') -> str:
        alias = get_uuid_name(suffix='zip')
        if model_description:
            image_txt = ImageName + '.txt'
            description_file: str = os.path.join(original_path, image_txt)

            with open(description_file, 'w') as f:
                f.write(model_description)

        # 压缩文件
        with zipfile.ZipFile(os.path.join(destination_path, alias), 'w', zipfile.ZIP_DEFLATED) as z:
            pre_len = len(os.path.dirname(original_path))
            for parent, dir_names, file_names in os.walk(original_path):
                for filename in file_names:
                    path_file = os.path.join(parent, filename)
                    arc_name = path_file[pre_len:].strip(os.path.sep)  # 相对路径
                    z.write(path_file, arc_name)
        return alias


class DockerImageService(object):

    @staticmethod
    def get_image(short_id: str):
        return DockerClient.get_image_by_id(short_id=short_id)

    @classmethod
    def save(cls, image_file: str, short_id: str = None, tags: str = None):
        if not any([short_id, tags]):
            raise ParameterError
        if short_id:
            image = DockerClient.get_image_by_id(short_id=short_id)
        else:
            image = DockerClient.get_image_by_tag(tags=tags)
        data = image.save(named=True)
        with open(image_file, 'wb') as f:
            for trunk in data:
                f.write(trunk)

    @classmethod
    def create_single_model(cls, model_id: int):
        docker_file_directory: str = None
        try:
            docker_file_directory = ModelDataPackageService.create(models_id=[model_id])
            image = DockerClient.build_image(path=docker_file_directory)
            return image
        except Exception:
            raise
        finally:
            if docker_file_directory:
                shutil.rmtree(docker_file_directory, True)

    @staticmethod
    def create_plural_models(modes_id: list):
        docker_file_directory: str = None
        try:
            docker_file_directory = ModelDataPackageService.create(models_id=modes_id)
            image = DockerClient.build_image(path=docker_file_directory)
            return image
        except Exception:
            raise
        finally:
            if docker_file_directory:
                shutil.rmtree(docker_file_directory, True)

    @staticmethod
    def remove(short_id: str):
        """
        $ docker rmi -f short_id
        """
        c = DockerClient.get_client()
        try:
            c.images.remove(image=short_id, force=True)
        except ImageNotFound:
            pass
            # raise DockerImageNotFoundError(ErrorMsg.get_error_message(40))

    @classmethod
    def delete_old(cls, image: DockerImage):
        image_file: str = image.alias
        if image_file:
            DataFileOperator(address='docker').delete(file_name=image.alias)
        try:
            cls.remove(short_id=image.short_id)
        except DockerContainerNotFoundError:
            pass
        db.session.delete(image)
        db.session.commit()

    @classmethod
    def delete(cls, image):
        try:
            cls.remove(short_id=image.short_id)
        except DockerContainerNotFoundError:
            pass

    @classmethod
    def package(cls, docker_image, model_description: str) -> str:
        alias = get_uuid_name(suffix='zip')
        image_directory = os.path.join(DataDirectoryPath.get_docker_image_path(), alias.split('.')[0])
        DataDirectoryPath.make_dirs(image_directory)
        try:
            image_tar = docker_image.tags[0] + '.tar'
            image_txt = ImageName + '.txt'
            image_file: str = os.path.join(image_directory, image_tar)
            description_file: str = os.path.join(image_directory, image_txt)

            cls.save(short_id=docker_image.short_id, image_file=image_file)
            with open(description_file, 'w') as f:
                f.write(model_description)

            # 压缩文件
            with zipfile.ZipFile(os.path.join(DataDirectoryPath.get_docker_image_path(), alias), 'w',
                                 zipfile.ZIP_DEFLATED) as z:
                z.write(image_file, image_tar)
                z.write(description_file, image_txt)
            return alias
        except Exception:
            if os.path.exists(os.path.join(DataDirectoryPath.get_docker_image_path(), alias)):
                os.remove(os.path.join(DataDirectoryPath.get_docker_image_path(), alias))
            raise
        finally:
            # 删除文件夹
            shutil.rmtree(image_directory, True)
