#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/23 17:06
# @Author : wangweimin
# @File   : model_train_task.py
# @Desc   :


import importlib
import os
import time
import traceback

from sklearn.pipeline import Pipeline

# Todo
# from app.celery_app import db, celery
from app import db
from app.main.modeling.modeling.i_model import IPreProcessing
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.main.services.operator.base_common.websocket_operator.websocket_operator import WebSocketService
from app.models import ModelFile, ModelVersion, Model, ModelDataFormat
from app.tasks_celery.tasks_base.socketio_requests import SocketIORequestsService
from conf.data_path import DataDirectoryPath


def model_save(model_id: int, pipe: Pipeline, **kwargs) -> bool:
    model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
    model_version: ModelVersion = model.model_version.first()
    if model_version.model_file is None:
        model_file_alias = get_uuid_name(suffix='pkl')
        model_file = ModelFile(alias=model_file_alias)
        db.session.add(model_file)
        db.session.commit()
        model_version.model_file = model_file
        db.session.commit()
    else:
        model_file: ModelFile = model_version.model_file
        model_file_alias = model_file.alias
    if model_version.data_format is None:
        model_data_format_alias = get_uuid_name(suffix='json')
        model_data_format = ModelDataFormat(alias=model_data_format_alias)
        db.session.add(model_data_format)
        db.session.commit()
        model_version.data_format = model_data_format
        db.session.commit()
    else:
        model_data_format_alias = model_version.data_format.alias
    if pipe is not None:
        try:
            if isinstance(pipe, Pipeline):
                model_file_alias = model_file_alias.split('.')[0] + '.pkl'
                model_version.model_type_id = 1
            elif os.path.isdir(pipe):
                model_file_alias = model_file_alias.split('.')[0] + '.gb'
                model_version.model_type_id = 2
            DataFileOperator(address='file').put(data=pipe, file_name=model_file_alias,
                                                 output_node_names=kwargs.get('output_node_names'))
            model_file.alias = model_file_alias
            db.session.commit()
            if isinstance(pipe, Pipeline):
                preprocessing = list(pipe.named_steps.values())[0]
                if isinstance(preprocessing, IPreProcessing):
                    data_format: dict = preprocessing.format
                else:
                    data_format: dict = {
                        'Waring': 'The first pipe of PipeLine needed to be PreProcessing type to check data format'}
                DataFileOperator(address='format').put(data=data_format, file_name=model_data_format_alias)
            model_version.status_id = 2
            db.session.commit()
            return True
        except Exception:
            model_version.status_id = 1
            db.session.commit()
            raise
        finally:
            # Todo
            # socket
            # SocketIORequestsService.refresh_project(project_id=model.project_id, address='model')
            WebSocketService.emit(event='refresh', address='model', project_id=model.project_id)
    else:
        DataFileOperator(address='file').truncate(file_name=model_file_alias)
        DataFileOperator(address='format').truncate(file_name=model_data_format_alias)
        model_version.model_type_id = None
        db.session.commit()
        return False


# @celery.task
def model_train(model_id: int):
    model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
    # ageing_docker_image(model_id=model_id)
    model_name = model.name
    model_version: ModelVersion = model.model_version.first()
    model_src_alias: str = model_version.model_source_code.alias
    model_info_alias: str = model_version.model_info.alias
    info = {}
    model_src_name = model_src_alias.rstrip('.py')
    try:
        module = ModelModuleService.get_module(model_src_name=model_src_name)
        if hasattr(module, 'build_and_train'):
            func = getattr(module, 'build_and_train')
            func_result = func()
            if not isinstance(func_result, tuple) or len(func_result) != 2:
                raise TypeError('Don\'t modify the return value of build_and_train func')
            mi, pipe = func_result
            info = mi.info
        else:
            raise ImportError('Can\'t find func called build_and_train in {}!'.format(model_name))
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
    model_save(model_id=model_id, pipe=pipe)


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
