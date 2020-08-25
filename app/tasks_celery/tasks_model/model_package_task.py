#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/1/3 10:14
# @Author : wangweimin
# @File   : model_package_task.py
# @Desc   :

# Todo
# from app.celery_app import celery, db
from app import db
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.docker_base_operator.docker_actual_image_operator import \
    ModelDataPackageService
from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.main.services.operator.base_common.websocket_operator.websocket_operator import WebSocketService
from app.models import ModelVersion, Model, ModelPackage, BaseDockerImage
from app.tasks_celery.tasks_base.socketio_requests import SocketIORequestsService
from conf.data_path import DataDirectoryPath

DockerDescription = "Download docker image '{}' first and load it with command: 'docker load -i xxx.tar'\n" \
                    "If you have loaded it, ignore this step.\n\n" \
                    "Unzip the zip file.\n" \
                    "Start up container with command:\ndocker run -d -p <your_port>:5000 " \
                    "--name=<container_name> -v /path/to/unzip/directory/data:/app/data {}\n" \
                    "Url interface is \"http://ip:port/predict\"\n\n"

ModelDescription = "Model: {}\t\tDescription: {}" \
                   "Data to predicted needed to satisfy below data format:\n{}\n\n" \
                   "the way to use like:" \
                   "curl 'http://ip:port/predict?model={}' -F 'file=@/path/to/data.csv'\n\n"

ResponseDescription = "The response data is a json type like \n" \
                      "{'code': 0, 'data': [{ 'result': 1 }, { 'result': 2 }] } " \
                      "or {'code': 1, 'message': { 'Error': 'xxx' } }"


# @celery.task
def model_package(model_id: int, user_id: int):
    model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
    model_version: ModelVersion = model.model_version.first()
    model_version.status_id = 7
    db.session.commit()
    SocketIORequestsService.refresh_project(project_id=model.project_id, address='model')

    # 开始打包
    model_package_directory: str = None
    try:
        model_package_directory, model_type_final = ModelDataPackageService.model_package(model_id=model_id)
        base_image: BaseDockerImage = BaseDockerImage.query.get(model_type_final)
        model_description = DockerDescription.format(base_image.name, base_image.tags)
        data_format_alias: str = model_version.data_format.alias
        data_format = DataFileOperator(address='format').get(filename=data_format_alias)
        model_description += ModelDescription.format(model.name, model.description, data_format, model.name)
        model_description += ResponseDescription
        # 打包压缩数据

        alias: str = ModelDataPackageService.zip(original_path=model_package_directory,
                                                 destination_path=DataDirectoryPath.get_model_package_path(),
                                                 model_description=model_description)

        model_package_: ModelPackage = ModelPackage(alias=alias)
        db.session.add(model_package_)
        db.session.commit()
        model_version.status_id = 5
        model_version.model_package_id = model_package_.id
        db.session.commit()

        return True
    except Exception:
        model_version.status_id = 6
        db.session.commit()
        # Todo
        # 先返回报错信息
        import traceback
        print(traceback.format_exc())
        raise  # ValueError("打包失败")
    finally:
        DataDirectoryPath.rm_dirs(path=model_package_directory)
        # Todo
        # socket
        # SocketIORequestsService.refresh_project(project_id=model.project_id, address='model')
        WebSocketService.emit(event='refresh', address='model', project_id=model.project_id)
