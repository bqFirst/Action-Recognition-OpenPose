#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/22 9:36
# @Author : wangweimin
# @File   : model_data_format_operator.py
# @Desc   :

from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.models import Model, ModelVersion, ModelDataFormat


class ModelDataFormatService(object):

    @classmethod
    def get(cls, model_id: int):
        model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
        model_version: ModelVersion = model.model_version.first()
        model_data_format: ModelDataFormat = model_version.data_format
        data_format = DataFileOperator(address='format').get(filename=model_data_format.alias)
        return data_format
