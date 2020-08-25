#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/2/10 16:37
# @Author : wangweimin
# @File   : case_task_operator.py
# @Desc   :

import os
from werkzeug.datastructures import FileStorage

from app.main.basic_main.custom_error import ParameterError, UserOperatorError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.main.services.operator.base_common.url_compose import CaseUrlCompose
from app.main.services.operator.docker_operator.docker_container_request_operator import DockerContainerRequestService
from app.models import Case, DockerContainer, DockerModelMode  # , InputParam, OutputParam
from conf.data_path import DataDirectoryPath


class CaseTaskService(object):
    FileType = ['picture', 'video']
    ReadNeededType = ['json']  # 返回结果数据需要读取
    PictureType = ['jpg', 'jpeg', 'png', 'bmp']
    VideoType = ['mp4', 'avi', 'mkv', 'mov', 'rmvb', 'flv']

    @classmethod
    def __allowed_picture(cls, picture_name: str) -> bool:
        return '.' in picture_name and picture_name.rsplit('.', 1)[1].lower() in cls.PictureType

    @classmethod
    def __allowed_video(cls, video_name: str) -> bool:
        return '.' in video_name and video_name.rsplit('.', 1)[1].lower() in cls.VideoType

    @classmethod
    def __allowed_file(cls, param_type: str, filename: str):
        is_allowed: bool = False
        if 'picture' == param_type:
            is_allowed = cls.__allowed_picture(filename)
        elif 'video' == param_type:
            is_allowed = cls.__allowed_video(filename)
        else:
            pass
        if not is_allowed:
            raise UserOperatorError(ErrorMsg.get_error_message(64))

    @classmethod
    def analyse_form_data(cls, input_params: list, form_data: dict, file_data: dict) -> dict:
        data: dict = dict()
        for input_param in input_params:
            # input_param: InputParam = input_param
            param_name: str = input_param.name
            param_type: str = input_param.param_type.name
            try:
                if param_type in cls.FileType:
                    file: FileStorage = file_data[param_name]
                    cls.__allowed_file(param_type=param_type, filename=file.filename)
                    suffix = file.filename.rsplit('.', 1)[-1]
                    suffix = suffix.lower()
                    filename: str = get_uuid_name(suffix=suffix)
                    file.save(os.path.join(DataDirectoryPath.get_case_path(), filename))
                    data[param_name] = filename
                else:
                    data[param_name] = form_data[param_name]
            except KeyError:
                if input_param.required:
                    raise ParameterError(ErrorMsg.get_error_message(63).format(param_name))
                else:
                    pass
        return data

    @classmethod
    def analyse_result_data(cls, output_params: list, result: dict) -> dict:
        result_data: dict = dict()
        for output_param in output_params:
            # output_param: OutputParam = output_param
            param_name: str = output_param.name
            param_type: str = output_param.param_type.name
            if param_type in cls.FileType:
                result_data[param_name] = CaseUrlCompose.case(alias=result[param_name])
            elif param_type in cls.ReadNeededType:
                result_data[param_name] = DataFileOperator(address='case').get(filename=result[param_name])
            else:
                result_data[param_name] = result[param_name]
        return result_data

    @classmethod
    def create(cls, case_id: int, mode_id: int, form_data: dict, file_data: dict):
        case: Case = ObjectAcquisition.case_by_id(case_id=case_id)
        docker_container: DockerContainer = case.container
        model_mode: DockerModelMode = ObjectAcquisition.mode_by_container(mode_id=mode_id,
                                                                          docker_container=docker_container)

        input_params: list = model_mode.input_params.all()
        form_data: dict = cls.analyse_form_data(input_params=input_params, form_data=form_data, file_data=file_data)
        form_data['mode_name'] = model_mode.name
        result: dict = DockerContainerRequestService.post_predict(docker_container=docker_container,
                                                                  form_data=form_data)

        output_params: list = model_mode.output_params.all()
        return cls.analyse_result_data(output_params=output_params, result=result)
