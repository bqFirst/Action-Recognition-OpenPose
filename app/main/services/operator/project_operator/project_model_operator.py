#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/4 15:34
# @Author : wangweimin
# @File   : project_model_operator.py
# @Desc   :

from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.models import Project, ModelStatus


class ProjectModelService(object):

    @classmethod
    def info(cls, project_id: int, model_status_id: str) -> list:
        project: Project = ObjectAcquisition.project_by_id(project_id=project_id)
        models: list = project.models.all()
        result = []
        for model in models:
            model_status: ModelStatus = model.model_version.first().model_status
            status_id = model_status.id
            if 0 == model_status_id or status_id == model_status_id:
                model_msg = dict()
                model_msg['model_id'] = model.id
                model_msg['create_time'] = model.create_time
                model_msg['model_name'] = model.name
                model_msg['status'] = model_status.name
                model_msg['creator'] = model.creator.name
                model_msg['description'] = model.description
                model_msg['model_status_id'] = status_id
                result.append(model_msg)
        return result
