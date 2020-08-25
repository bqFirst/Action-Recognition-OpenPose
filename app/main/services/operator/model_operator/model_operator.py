#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/7 10:34
# @Author : wangweimin
# @File   : model_operator.py
# @Desc   :

import os

from sqlalchemy import and_

from app import db
from app.main.basic_main.custom_error import UserOperatorError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectExistJudgement, \
    ObjectNameRepeatedJudgement
from app.main.services.operator.base_common.websocket_operator.websocket_operator import WebSocketService
from app.main.services.operator.model_operator.model_src_operator import ModelSrcService
from app.models import ModelFile, ModelInfo, ModelVersion, Model, ModelSourceCode, Project, ModelDataFormat, \
    ModelPackage
from app.tasks_celery.tasks_model.model_package_task import model_package
from app.tasks_celery.tasks_model.model_train_task import model_train
from conf.data_path import DataDirectoryPath


class ModelService(object):

    @staticmethod
    def __is_delete_legal(model_version: ModelVersion):
        # 判断能否删除
        status_id = model_version.status_id
        # 已生成镜像，无法删除
        if 3 == status_id:
            raise UserOperatorError(ErrorMsg.get_error_message(15))
        elif 7 == status_id:
            raise UserOperatorError(ErrorMsg.get_error_message(41))
        elif 5 == status_id:
            raise UserOperatorError(ErrorMsg.get_error_message(42))
        elif 2 == status_id:
            model: Model = model_version.model
            applications = model.applications.all()
            if applications:
                application_name_list = [application.name for application in applications]
                raise UserOperatorError(ErrorMsg.get_error_message(43).format('、'.join(application_name_list)))

    @classmethod
    def delete(cls, model_id: int) -> None:
        model: Model = ObjectAcquisition.model_by_id(model_id=model_id)

        model_version: ModelVersion = model.model_version.first()
        if model_version is None:
            db.session.delete(model)
            db.session.commit()
            return
        cls.__is_delete_legal(model_version=model_version)

        model_data_format: ModelDataFormat = model_version.data_format
        model_info: ModelInfo = model_version.model_info
        model_file: ModelFile = model_version.model_file
        model_src: ModelSourceCode = model_version.model_source_code

        if model_src is not None:
            DataFileOperator(address='src').delete(file_name=model_src.alias)
            db.session.delete(model_src)
        if model_file is not None:
            DataFileOperator(address='file').delete(file_name=model_file.alias)
            db.session.delete(model_file)
        if model_info is not None:
            DataFileOperator(address='info').delete(file_name=model_info.alias)
            db.session.delete(model_info)
        if model_data_format is not None:
            DataFileOperator(address='format').delete(file_name=model_data_format.alias)
            db.session.delete(model_data_format)

        db.session.delete(model_version)
        db.session.delete(model)
        db.session.commit()
        return

    @classmethod
    def download(cls, model_id: int, user_id: int, error=True) -> tuple:
        if error:
            raise UserOperatorError(ErrorMsg.get_error_message(67))
        model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
        model_version: ModelVersion = model.model_version.first()
        if model_version.status_id != 5:
            raise UserOperatorError(ErrorMsg.get_error_message(3))
        # short_id, image_id = get_image_info(model_id=model_id, user_id=user_id)
        # image_id = model_version.image_id
        # docker_image: DockerImage = DockerImage.query.get(image_id)
        # alias: str = docker_image.alias
        model_package_: ModelPackage = model_version.model_package
        alias: str = model_package_.alias

        # 如果该模型镜像已经被压缩成功过，则直接获取
        if isinstance(alias, str) and alias.endswith('.zip'):
            return DataDirectoryPath.get_model_package_path(), alias, model.name + '.zip'
            # return DataDirectoryPath.get_docker_image_path(), alias, model.name + '.zip'
        else:
            raise ValueError(ErrorMsg.get_error_message(4))

    @staticmethod
    def __is_package_legal(model_version: ModelVersion):
        if model_version.status_id == 1:
            raise UserOperatorError(ErrorMsg.get_error_message(5))
        if model_version.status_id == 3:
            raise UserOperatorError(ErrorMsg.get_error_message(6))
        if model_version.status_id == 7:
            raise UserOperatorError(ErrorMsg.get_error_message(7))
        if model_version.status_id == 5:
            raise UserOperatorError(ErrorMsg.get_error_message(8))

    @classmethod
    def package(cls, model_id: int, user_id: int, error=True) -> bool:
        if error:
            raise UserOperatorError(ErrorMsg.get_error_message(67))
        model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
        model_version: ModelVersion = model.model_version.first()
        cls.__is_package_legal(model_version=model_version)
        # Todo
        # model_package.delay(model_id, user_id)  # 异步任务
        model_package(model_id, user_id)  # 异步任务
        return True

    @classmethod
    def create_model_version(cls, project_id: int, user_id: int, model_name: str, description: str, src: str) -> int:
        project: Project = ObjectAcquisition.project_by_id(project_id=project_id)
        # 创建model
        model = Model(name=model_name, creator_id=user_id, project=project, description=description)
        db.session.add(model)
        db.session.commit()
        # 创建model_version
        # 1.1 复制模板py
        src_file = get_uuid_name(suffix='py')
        DataFileOperator(address='src').put(data=src, file_name=src_file)

        # 1.2 修改默认路径
        # src_content: str = DataFileOperator(address='src').get(filename=src_file)
        # project_path = get_project_path_by_id(project_id=project_id)
        # src_content = src_content.replace("project_path=''", "project_path='{}'".format(project_path))
        # DataFileOperator(address='src').put(data=src_content, file_name=src_file)

        model_src = ModelSourceCode(alias=src_file)
        db.session.add(model_src)
        db.session.commit()

        # 2. 写结果文件，默认为空
        model_info_file = get_uuid_name(suffix='json')
        DataFileOperator(address='info').put(data={}, file_name=model_info_file)
        model_info = ModelInfo(alias=model_info_file)
        db.session.add(model_info)
        db.session.commit()

        # 3. 写模型数据结构文件，默认为{}
        model_data_format_alias = get_uuid_name(suffix='json')
        DataFileOperator(address='format').put(data={}, file_name=model_data_format_alias)
        model_data_format = ModelDataFormat(alias=model_data_format_alias)
        db.session.add(model_data_format)
        db.session.commit()

        # 4. 写模型文件，仅创建文件
        model_file_alias = get_uuid_name(suffix='pkl')
        model_file = ModelFile(alias=model_file_alias)
        f = open(os.path.join(DataDirectoryPath.get_model_file_path(), model_file_alias), 'w')
        f.close()
        db.session.add(model_file)
        db.session.commit()

        # 5. 创建model_version
        model_version = ModelVersion(creator_id=user_id, model=model, model_source_code=model_src,
                                     model_info=model_info, data_format=model_data_format, model_file=model_file)
        db.session.add(model_version)
        db.session.commit()
        return model.id

    @staticmethod
    def __is_legal_to_train(model: Model) -> None:
        model_version: ModelVersion = model.model_version.first()
        if model_version.status_id == 3:
            raise UserOperatorError(ErrorMsg.get_error_message(15))
        if model_version.status_id == 7:
            raise UserOperatorError(ErrorMsg.get_error_message(16))
        if model_version.status_id == 5:
            raise UserOperatorError(ErrorMsg.get_error_message(17))
        if model.applications.first() is not None:
            raise UserOperatorError(ErrorMsg.get_error_message(69))

    @classmethod
    def create(cls, project_id: int, user_id: int, model_name: str, description: str, src: str) -> int:
        ObjectExistJudgement.project_id(project_id=project_id)
        model: Model = Model.query.filter(and_(Model.project_id == project_id, Model.name == model_name)).first()
        if model is None:
            ObjectExistJudgement.model_name(model_name=model_name, user_id=user_id)
            model_id: int = cls.create_model_version(project_id=project_id, user_id=user_id, model_name=model_name,
                                                     description=description, src=src)
        else:
            cls.__is_legal_to_train(model=model)
            model.description = description
            model_version: ModelVersion = model.model_version.first()
            model_version.status_id = 3
            db.session.commit()
            model_id: int = model.id
            ModelSrcService.preserve(model_id=model_id, new_src=src)
        WebSocketService.emit(event='refresh', address='model', project_id=project_id)
        # Todo
        # 异步任务
        # model_train.delay(model_id)
        model_train(model_id)
        return model_id

    @classmethod
    def get(cls, model_id: int) -> dict:
        model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
        model_version: ModelVersion = model.model_version.first()
        model_src: ModelSourceCode = model_version.model_source_code
        src: str = DataFileOperator(address='src').get(filename=model_src.alias)
        model_data_format: ModelDataFormat = model_version.data_format
        data_format = DataFileOperator(address='format').get(filename=model_data_format.alias)
        return {'model_name': model.name, 'description': model.description, 'model_id': model_id, 'src': src,
                'data_format': str(data_format)}

    @classmethod
    def rename(cls, model_id: int, model_name: str):
        # Todo
        # 模型一旦被使用，无法修改名称/未实现完毕
        model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
        if model.name != model_name:
            ObjectNameRepeatedJudgement.model_by_project_id(model_name=model_name, user_id=model.creator_id)
        model.name = model_name
        db.session.commit()
