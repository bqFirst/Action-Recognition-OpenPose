#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/23 10:26
# @Author : wangweimin
# @File   : docker_package_task.py
# @Desc   :

from app.celery_app import celery, db
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.docker_base_operator.docker_actual_image_operator import DockerImageService
from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.models import ModelVersion, Model, DockerImage, Application
from app.tasks_celery.tasks_base.socketio_requests import SocketIORequestsService

ModelDescription = "Load docker image with command: 'docker load -i xxx.tar'\n" \
                   "After loaded successfully, start up container with command:\ndocker run -d -p <your_port>:5000 " \
                   "--name=<container_name> <image_name>:<image_version>\n" \
                   "Data to predicted needed to satisfy below data format:\n%s\n\n" \
                   "Url interface is \"http://ip:port/predict\" and send data use:\n" \
                   "curl 'http://ip:port/predict?model=%s' -F 'data=@/path/to/data.csv'\n\n" \
                   "The response data is a json type like \n" \
                   "{'code': 0, 'data': [{ 'result': 1 }, { 'result': 2 }] } " \
                   "or {'code': 1, 'message': { 'Error': 'xxx' } }"


@celery.task
def model_docker_package(model_id: int, user_id: int):
    model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
    model_version: ModelVersion = model.model_version.first()
    model_version.status_id = 7
    db.session.commit()

    # 开始打包
    docker_image: DockerImage = None
    try:
        image = DockerImageService.create_single_model(model_id=model_id)
        tags = image.tags[0]
        short_id = image.short_id
        docker_image: DockerImage = DockerImage(tags=tags, short_id=short_id, creator_id=user_id, status_id=2)
        db.session.add(docker_image)
        db.session.commit()

        data_format_alias: str = model_version.data_format.alias
        data_format = DataFileOperator(address='format').get(filename=data_format_alias)
        model_description: str = ModelDescription % (data_format, model.name)
        DockerImageService.package(docker_image=docker_image, model_description=model_description)
        model_version.status_id = 5
        model_version.image_id = docker_image.id
        db.session.commit()
        # 单模型镜像不会用于启动容器，因此删除掉
        DockerImageService.remove(short_id=short_id)
        return True
    except Exception:
        model_version.status_id = 6
        db.session.commit()
        if docker_image:
            db.session.delete(docker_image)
            db.session.commit()
        # Todo
        # 先返回报错信息
        raise  # ValueError("打包失败")
    finally:
        SocketIORequestsService.refresh_project(project_id=model.project_id, address='model')


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


@celery.task
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
    SocketIORequestsService.refresh_application(application_id=application_id)
