#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/1/9 0009 15:34
# @Author : wangw
# @File   : model_src_operator.py
# @Desc   :

import os
import re

from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.models import Model
from conf.data_path import DataDirectoryPath
from conf.system_config import PylintCommand

EFMatch = re.compile('[EF].*')
FuncMatch = re.compile('build_and_train\((.*)\)')
ModelPredictMatch = re.compile('ModelPredict\((.*)\)')
ParameterMatch = re.compile(',\s+?')


class ModelSrcService(object):

    @classmethod
    def verify(cls, src: str) -> str:
        pass

    @classmethod
    def preserve(cls, model_id: int, new_src: str):
        model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
        model_src_alias = model.model_version.first().model_source_code.alias
        # 覆盖原有文件
        # Todo
        DataFileOperator(address='src').put(data=new_src, file_name=model_src_alias)
        return

    @classmethod
    def get(cls, model_id: int) -> str:
        pass