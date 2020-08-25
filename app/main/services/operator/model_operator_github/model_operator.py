#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/1/9 0009 15:34
# @Author : wangw
# @File   : model_operator.py
# @Desc   :

import importlib
import os
import time
import traceback
import subprocess

from sqlalchemy import and_

from app import db
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectExistJudgement
from app.main.services.operator.model_operator_github.model_src_operator import ModelSrcService
from app.models import ModelFile, ModelInfo, ModelVersion, Model, ModelSourceCode, Project, ModelDataFormat
from conf.data_path import DataDirectoryPath

from app.main.services.operator.model_operator.model_operator import ModelService

ModelDescription = "Load docker image with command: 'docker load -i xxx.tar'\n" \
                   "After loaded successfully, start up container with command:\n'docker run -d -p <your_port>:5000 " \
                   "--name=<container_name> <image_name>:<image_version>'\n" \
                   "Data to predicted needed to satisfy below data format:\n%s\n\n" \
                   "Url interface is \"http://ip:port/predict\" and send data use:\n" \
                   "curl 'http://ip:port/predict?model=%s' -F 'data=@/path/to/data.csv'\n\n" \
                   "The response data is a json type like \n" \
                   "{'code': 0, 'data': [{ 'result': 1 }, { 'result': 2 }] } " \
                   "or {'code': 1, 'message': { 'Error': 'xxx' } }"


class ModelTfService(ModelService):

    @classmethod
    def train(cls, model_id: int) -> str:
        model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
        # ageing_docker_image(model_id=model_id)
        model_version: ModelVersion = model.model_version.first()
        model_src_alias: str = model_version.model_source_code.alias
        model_info_alias: str = model_version.model_info.alias
        info = {}
        ckpt_dir = None

        model_version.status_id = 3
        db.session.commit()

        try:
            path = os.path.join(DataDirectoryPath.get_module_path(), model_src_alias)
            fun = os.path.join(path, 'train.py')

            p = subprocess.Popen('cd' + ' ' + path + ' ' + '&&' + ' ' + 'python train.py', shell=True)
            p.wait()
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.split('.')[-1] == 'meta':
                        ckpt_dir = root
            model_version.status_id = 2
            db.session.commit()

        except Exception:
            model_version.status_id = 1
            db.session.commit()
            model_file: ModelFile = model_version.model_file
            DataFileOperator(address='file').truncate(file_name=model_file.alias)
            model_data_format: ModelDataFormat = model_version.data_format
            DataFileOperator(address='format').truncate(file_name=model_data_format.alias)
            model_version.model_type_id = None
            db.session.commit()
            info['_PROGRAM_ERROR_'] = traceback.format_exc()
            raise
        finally:
            if not info:
                info['MSG'] = 'Nothing'
            DataFileOperator(address='info').put(data=info, file_name=model_info_alias)
        return ckpt_dir

    # @staticmethod
    # def __is_delete_legal(model_version: ModelVersion):
    #     # 判断能否删除
    #     status_id = model_version.status_id
    #     # 已生成镜像，无法删除
    #     if 3 == status_id:
    #         raise UserOperatorError(ErrorMsg.get_error_message(15))
    #     elif 7 == status_id:
    #         raise UserOperatorError(ErrorMsg.get_error_message(41))
    #     elif 5 == status_id:
    #         raise UserOperatorError(ErrorMsg.get_error_message(42))
    #     elif 2 == status_id:
    #         model: Model = model_version.model
    #         applications = model.applications.all()
    #         if applications:
    #             application_name_list = [application.name for application in applications]
    #             raise UserOperatorError(ErrorMsg.get_error_message(43).format('、'.join(application_name_list)))

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
    def create_model_version(cls, project_id: int, user_id: int, model_name: str, description: str, src: str) -> int:
        """

        :param project_id:
        :param user_id:
        :param model_name:
        :param description:
        :param src: 项目文件夹
        :return:
        """
        project: Project = ObjectAcquisition.project_by_id(project_id=project_id)
        # 创建model
        model = Model(name=model_name, creator_id=user_id, project=project, description=description)
        db.session.add(model)
        db.session.commit()
        # 创建model_version

        # 1.1 创建一个文件夹
        src_file = get_uuid_name()  # 创建一个文件夹
        # 将文件复制到folder
        DataFileOperator(address='src').put(data=src, file_name=src_file)

        # 1.2 修改默认路径
        # src_content: str = DataFileOperator(address='src').get(filename=src_file)
        # project_path = get_project_path_by_id(project_id=project_id)
        # src_content = src_content.replace("project_path=''", "project_path='{}'".format(project_path))
        # DataFileOperator(address='src').put(data=src_content, file_name=src_file)
        model_src = ModelSourceCode(alias=src_file)  # 记录的是文件夹alias
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
        model_file_alias = get_uuid_name(suffix='gb')
        model_file = ModelFile(alias=model_file_alias)
        f = open(os.path.join(DataDirectoryPath.get_model_file_path(), model_file_alias), 'w')
        f.close()
        db.session.add(model_file)
        db.session.commit()

        # 5. 创建model_version
        model_version = ModelVersion(status_id=2, creator_id=user_id, model=model, model_source_code=model_src,
                                     model_info=model_info, data_format=model_data_format, model_file=model_file)
        model_version.model_type_id = 2
        db.session.add(model_version)
        db.session.commit()
        return model.id

    @classmethod
    def create_github(cls, project_id: int, model_name: str, user_id: int, path: str, description: str, shell: list):
        """

        :param project_id:
        :param user_id:
        :param model_name:
        :param description:
        :param path: jupyter文件路径
        :param shell:
        :return:
        """
        ObjectExistJudgement.project_id(project_id=project_id)
        model: Model = Model.query.filter(and_(Model.project_id == project_id, Model.name == model_name)).first()
        if model is None:
            ObjectExistJudgement.model_name(model_name=model_name, user_id=user_id)
            model_id: int = cls.create_model_version(project_id=project_id, user_id=user_id, model_name=model_name,
                                                     description=description, src=path)
        else:
            # cls.is_legal_to_train(model=model)
            model.description = description
            model_version: ModelVersion = model.model_version.first()
            model_version.status_id = 2
            db.session.commit()
            model_id: int = model.id
            ModelSrcService.preserve(model_id=model_id, new_src=path)

        if shell:
            print("开始编译")
            cls.subprocess_shell(shell, model_id=model_id)
            print("Done!")
        #
        # ckpt_dir: str = cls.train(model_id=model_id)
        # cls.save(model_id=model_id, pipe=ckpt_dir, output_node_names='keep_prob_placeholder')
        return model_id

    @staticmethod
    def subprocess_shell(commands: list, model_id: int):
        model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
        model_version: ModelVersion = model.model_version.first()
        model_src_alias: str = model_version.model_source_code.alias

        for cmd in commands:
            subprocess.Popen('cd' + ' ' + model_src_alias + '&&' + cmd, shell=True)

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


class ModelModuleService(object):

    ModuleMap = dict()

    @classmethod
    def get_module(cls, model_src_name: str):
        module = cls.ModuleMap.get(model_src_name)
        if module is None:
            module = importlib.import_module(
                '.'.join(os.path.join(DataDirectoryPath.get_module_path(), model_src_name).split(os.path.sep)))
            cls.ModuleMap[model_src_name] = module
        else:
            importlib.reload(module)
            time.sleep(1)
        return module