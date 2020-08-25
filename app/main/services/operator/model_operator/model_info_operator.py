#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/22 9:32
# @Author : wangweimin
# @File   : model_info_operator.py
# @Desc   :

from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.models import Model, ModelVersion, ModelInfo


class ModelInfoService(object):

    @classmethod
    def get(cls, model_id: int):
        model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
        model_version: ModelVersion = model.model_version.first()
        model_info: ModelInfo = model_version.model_info
        info = DataFileOperator(address='info').get(filename=model_info.alias)
        return info
