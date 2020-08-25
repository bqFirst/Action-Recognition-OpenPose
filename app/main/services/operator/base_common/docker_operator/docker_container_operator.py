#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/2 17:25
# @Author : wangweimin
# @File   : docker_container_operator.py
# @Desc   :

from app import db

from app.main.basic_main.custom_error import DockerContainerNotFoundError
from app.main.services.operator.base_common.docker_operator.docker_client import DockerClient
from app.main.services.operator.base_common.docker_operator.docker_image_operator import DockerImageService
from app.models import DockerContainer, DockerImage, DockerPort


class DockerContainerService(object):

    @staticmethod
    def stop(short_id: str):
        container = DockerClient.get_container(short_id=short_id)
        container.stop()

    @staticmethod
    def start(short_id: str):
        container = DockerClient.get_container(short_id=short_id)
        container.start()

    @staticmethod
    def remove(short_id: str):
        """
        $ docker rm -f short_id
        """
        container = DockerClient.get_container(short_id=short_id)
        container.remove(force=True)

    @staticmethod
    def status(short_id: str) -> bool:
        container = DockerClient.get_container(short_id=short_id)
        status = container.status
        if 'running' == status:
            return True
        else:
            return False

    @classmethod
    def delete(cls, container: DockerContainer, keep_port=False):
        container_short_id = container.short_id
        try:
            cls.stop(short_id=container_short_id)
            cls.remove(short_id=container_short_id)
        except DockerContainerNotFoundError:
            pass
        image: DockerImage = container.image
        DockerImageService.delete(image=image)
        if not keep_port:
            server_port: DockerPort = container.docker_port
            db.session.delete(server_port)
            db.session.commit()
        db.session.delete(container)
        db.session.commit()
