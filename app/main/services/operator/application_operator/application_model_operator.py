#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/5 14:37
# @Author : wangwei
# @File   : application_model_operator.py
# @Desc   : 

from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.main.services.operator.task_operator.task_config import LinuxFileCurl
from app.models import Application, ModelVersion, Model


class ApplicationModelService(object):

    @classmethod
    def info(cls, application_id: int, model_status_id: str) -> list:
        application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
        models: list = application.models.order_by(Model.name).all()
        result = []
        port: int = application.port
        for model in models:
            model_version: ModelVersion = model.model_version.first()
            status_id = model_version.status_id
            if 0 == model_status_id or status_id == model_status_id:
                model_msg = dict()
                model_msg['model_id'] = model.id
                model_msg['model_name'] = model.name
                model_msg['model_status_id'] = status_id
                model_msg['description'] = model.description
                model_msg['api'] = LinuxFileCurl.format(port, model.name)
                model_msg['project_name'] = model.project.name
                result.append(model_msg)
        return result
