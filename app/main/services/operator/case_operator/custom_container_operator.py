#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/2/4 16:49
# @Author : wangweimin
# @File   : custom_container_operator.py
# @Desc   :

import requests
from typing import Tuple

from app import db
from app.main.basic_main.custom_error import DockerContainerCheckError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.main.services.operator.base_common.docker_base_operator.docker_actual_container_operator import \
    DockerContainerService
from app.models import CaseDockerContainer, DockerPort, DockerModelMode, InputParam, OutputParam, ParamType, \
    DockerModelAssessment
from .case_config import ParamUrl, InitUrl


class CustomContainerService(object):

    @staticmethod
    def check_container(short_id: str, port: int) -> dict:
        if not DockerContainerService.status(short_id=short_id):
            raise DockerContainerCheckError(ErrorMsg.get_error_message(58))
        try:
            response = requests.get(InitUrl.format(port))
            param_response = requests.get(ParamUrl.format(port))
        except Exception:
            raise DockerContainerCheckError(ErrorMsg.get_error_message(59))
        result: dict = response.json()
        if result['code']:
            raise DockerContainerCheckError(
                ErrorMsg.get_error_message(60) + ' {}'.format(result.get('message').get('Error')))
        # 获取参数
        param_result = param_response.json()
        if param_result.get('code'):
            raise DockerContainerCheckError(ErrorMsg.get_error_message(60))
        return param_result

    @classmethod
    def create(cls, short_id: str, port: int) -> Tuple[CaseDockerContainer, str]:
        result: dict = cls.check_container(short_id=short_id, port=port)
        docker_port: DockerPort = DockerPort(port=port)
        db.session.add(docker_port)
        db.session.commit()
        docker_container: CaseDockerContainer = CaseDockerContainer(name=result.get('name', ''), short_id=short_id,
                                                                    docker_port_id=docker_port.id)
        db.session.add(docker_container)
        db.session.commit()

        try:
            params = result.get('param')
            if len(params) == 0:
                raise DockerContainerCheckError(ErrorMsg.get_error_message(61))
            for mode_param in params:
                param: dict = mode_param.get('param')
                input_params: list = param.get('input')
                output_params: list = param.get('output')
                if not all([input_params, output_params]):
                    raise DockerContainerCheckError(ErrorMsg.get_error_message(61))
                mode_name = mode_param.get('mode')
                model_mode: DockerModelMode = DockerModelMode(name=mode_name, container_id=docker_container.id)
                db.session.add(model_mode)
                db.session.commit()
                for input_param in input_params:
                    param_name = input_param.get('name')
                    param_type = input_param.get('type')
                    if not all([param_name, param_type]):
                        raise DockerContainerCheckError(ErrorMsg.get_error_message(61))
                    i_param: InputParam = InputParam(name=param_name, description=input_param.get('description', ''),
                                                     required=input_param.get('required'), mode=model_mode,
                                                     param_type=ParamTypeService.get_param_type(param_type=param_type))
                    db.session.add(i_param)
                    db.session.commit()

                for output_param in output_params:
                    param_name = output_param.get('name')
                    param_type = output_param.get('type')
                    if not all([param_name, param_type]):
                        raise DockerContainerCheckError(ErrorMsg.get_error_message(61))
                    o_param: OutputParam = OutputParam(name=param_name, description=output_param.get('description', ''),
                                                       mode=model_mode,
                                                       param_type=ParamTypeService.get_param_type(
                                                           param_type=param_type))
                    db.session.add(o_param)
                    db.session.commit()
        except Exception:
            db.session.delete(docker_port)
            db.session.delete(docker_container)
            db.session.commit()
            raise
        model_assessment: dict = result.get('assessment')
        if model_assessment:
            db.session.execute(DockerModelAssessment.__table__.insert(),
                               [{'attribute': attribute, 'value': value, 'container_id': docker_container.id} for
                                attribute, value in model_assessment.items()]
                               )
            db.session.commit()
        return docker_container, result.get('key')

    @classmethod
    def delete(cls, docker_container: CaseDockerContainer):
        docker_port: DockerPort = docker_container.docker_port

        docker_container.model_assessment.delete()
        for model_mode in docker_container.model_mode.all():
            model_mode.input_params.delete()
            model_mode.output_params.delete()
            db.session.delete(model_mode)
        db.session.delete(docker_container)
        db.session.delete(docker_port)
        db.session.commit()


class ParamTypeService(object):
    ParamMap: dict = {}

    @classmethod
    def get_param_type(cls, param_type: str) -> ParamType:
        try:
            return cls.ParamMap[param_type]
        except KeyError:
            param_type_ = ObjectAcquisition.param_type(param_type=param_type)
            cls.ParamMap[param_type] = param_type_
            return param_type_
