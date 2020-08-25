#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/29 15:09
# @Author : wangweimin
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
        file = get_uuid_name(suffix='py')
        DataFileOperator(address='src').put(data=src, file_name=file)
        try:
            checked_file: str = os.path.join(DataDirectoryPath.get_model_src_path(), file)
            with os.popen(r'{} -E --reports=n {}'.format(PylintCommand.command(), checked_file), 'r') as f:
                check_info = f.read()
            result: list = EFMatch.findall(check_info)
            match = FuncMatch.search(src)
            if not match:
                result.append('F: Can\'t find func build_and_train')
            else:
                # 若函数存在，判断是否只传递了默认参数
                parameters = match.group(1).strip()
                if parameters:
                    params: list = ParameterMatch.split(parameters)
                    for param in params:
                        if '=' not in param:
                            result.append('F: Func build_and_train only support default parameters')
                            break
            match = ModelPredictMatch.search(src)
            if not match:
                result.append('F: Can\'t find class ModelPredict')
            else:
                # 若函数存在，判断是否继承了基类
                parameters = match.group(1).strip()
                if parameters:
                    params: list = ParameterMatch.split(parameters)
                    is_exist: bool = False
                    for param in params:
                        if 'IModelPredict' == param:
                            is_exist = True
                            break
                    if not is_exist:
                        result.append('F: Class ModelPredict need IModelPredict. default parameters')
            return '\n'.join(result)
        except Exception:
            raise
        finally:
            DataFileOperator(address='src').delete(file_name=file)

    @classmethod
    def preserve(cls, model_id: int, new_src: str):
        model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
        model_src_alias = model.model_version.first().model_source_code.alias
        DataFileOperator(address='src').put(data=new_src, file_name=model_src_alias)
        return

    @classmethod
    def get(cls, model_id: int) -> str:
        model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
        model_src_alias = model.model_version.first().model_source_code.alias
        return DataFileOperator(address='src').get(filename=model_src_alias)