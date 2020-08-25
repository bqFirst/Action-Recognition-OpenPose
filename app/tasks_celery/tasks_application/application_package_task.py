#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/1/7 17:39
# @Author : wangweimin
# @File   : application_package_task.py
# @Desc   :

import os

# Todo
# from app.celery_app import celery, db
from app import db
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.docker_base_operator.docker_actual_image_operator import DockerImageService
from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.main.services.operator.base_common.websocket_operator.websocket_operator import WebSocketService
from app.models import DockerImage, Application, DockerImageFile
from app.tasks_celery.tasks_base.socketio_requests import SocketIORequestsService
from conf.data_path import DataDirectoryPath


DockerDescription = "Load docker image with command: 'docker load -i xxx.tar'\n" \
                    "After loaded successfully, start up container with command:\n'docker run -d -p <your_port>:5000 " \
                    "--name=<container_name> <image_name>:<image_version>'\n" \
                    "Url interface is \"http://ip:port/predict\"\n and there are {} models to use:\n\n"

ModelDescription2 = "Model: {}\t\tDescription: {}" \
                   "Data to predicted needed to satisfy below data format:\n{}\n\n" \
                   "the way to use like:" \
                   "curl 'http://ip:port/predict?model={}' -F 'file=@/path/to/data.csv'\n\n"

ResponseDescription = "The response data is a json type like \n" \
                      "{'code': 0, 'data': [{ 'result': 1 }, { 'result': 2 }] } " \
                      "or {'code': 1, 'message': { 'Error': 'xxx' } }"


# @celery.task
def application_docker_package(application_id: int):
    application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
    docker_image: DockerImage = application.container.image
    docker_image.status_id = 2
    db.session.commit()
    models: list = application.models.all()

    model_description = DockerDescription.format(len(models))
    for model in models:
        data_format_alias: str = model.model_version.first().data_format.alias
        data_format = DataFileOperator(address='format').get(filename=data_format_alias)
        model_description += ModelDescription2.format(model.name, model.description, data_format, model.name)
    model_description += ResponseDescription
    DockerImageService.package(docker_image=docker_image, model_description=model_description)  # 包含状态改变
    # Todo
    # SocketIORequestsService.refresh_application(application_id=application_id)
    WebSocketService.emit(event='refresh', address='application', application_id=application_id)


# @celery.task
def application_package(application_id: int):
    application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
    docker_image: DockerImageFile = application.application_image
    docker_image.status_id = 2
    db.session.commit()

    # Todo
    # SocketIORequestsService.refresh_application(application_id=application_id)
    WebSocketService.emit(event='refresh', address='application', application_id=application_id)
    image = None
    alias = None
    try:
        models: list = application.models.all()
        image = DockerImageService.create_plural_models(modes_id=[model.id for model in models])

        model_description = DockerDescription.format(len(models))
        for model in models:
            data_format_alias: str = model.model_version.first().data_format.alias
            data_format = DataFileOperator(address='format').get(filename=data_format_alias)
            model_description += ModelDescription2.format(model.name, model.description, data_format, model.name)
        model_description += ResponseDescription
        alias: str = DockerImageService.package(docker_image=image, model_description=model_description)
        docker_image.alias = alias
        docker_image.status_id = 3
        db.session.commit()
    except Exception:
        docker_image.status_id = 1
        db.session.commit()
        if alias:
            os.remove(os.path.join(DataDirectoryPath.get_docker_image_path(), alias))
        raise
    finally:
        if image:
            DockerImageService.delete(image=image)
        # Todo
        # SocketIORequestsService.refresh_application(application_id=application_id)
        WebSocketService.emit(event='refresh', address='application', application_id=application_id)
