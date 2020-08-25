#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/2 11:26
# @Author : wangweimin
# @File   : docker_client.py
# @Desc   :

import random
import docker
import time
import threading

from docker.errors import NotFound, ImageNotFound, APIError

from app.main.basic_main.custom_error import PortExhaustionError, DockerContainerNotFoundError, DockerImageNotFoundError
from app.main.basic_main.error_message import ErrorMsg
from app.models import DockerPort


from app.main.basic_main.custom_error import ParameterError


class DockerClient(object):
    client: docker.client.DockerClient = None

    @classmethod
    def init(cls) -> None:
        cls.client = docker.from_env()

    @classmethod
    def get_client(cls):
        if not isinstance(cls.client, docker.client.DockerClient):
            cls.init()
        return cls.client

    @classmethod
    def get_image_by_tag(cls, tags: str):
        c = cls.get_client()
        try:
            return c.images.get(tags)
        except ImageNotFound:
            raise DockerImageNotFoundError(ErrorMsg.get_error_message(40))

    @classmethod
    def get_image_by_id(cls, short_id: str):
        c = cls.get_client()
        try:
            return c.images.get(short_id)
        except ImageNotFound:
            raise DockerImageNotFoundError(ErrorMsg.get_error_message(40))

    @classmethod
    def build_image(cls, path: str):
        c = cls.get_client()
        image, log = c.images.build(path=path, tag='myflask:v{}'.format(int(time.time())))
        return image

    @staticmethod
    def run_container(image_short_id: str, appoint_port: int=None):
        c = DockerClient.get_client()
        if appoint_port:
            port = appoint_port
        else:
            port = ServerPortManager.get_available_port()
        while True:
            try:
                container = c.containers.run(image_short_id, detach=True, ports={'5000/tcp': port})
                break
            except APIError as e:
                # 指定窗口出错
                if appoint_port:
                    raise
                # 并非端口被占用
                if 'port is already allocated' not in str(e):
                    raise
                ServerPortManager.add_unavailable_port(port=port)  # 增加不可用端口
                port = ServerPortManager.get_available_port()
        return port, container

    @classmethod
    def get_container(cls, short_id: str=None, name: str=None):
        if not any([short_id, name]):
            raise ParameterError('参数错误')
        if short_id:
            return cls.__get_container_by_id(short_id=short_id)
        else:
            return cls.__get_container_by_name(name=name)

    @classmethod
    def __get_container_by_id(cls, short_id: str):
        c = cls.get_client()
        try:
            return c.containers.get(short_id)
        except NotFound:
            raise DockerContainerNotFoundError(ErrorMsg.get_error_message(39))

    @classmethod
    def __get_container_by_name(cls, name: str):
        c = cls.get_client()
        try:
            return c.containers.get(name)
        except NotFound:
            raise DockerContainerNotFoundError(ErrorMsg.get_error_message(39))


class ServerPortManager(object):
    Lock = threading.Lock()
    OpenPort = set(range(8000, 10001))

    @classmethod
    def get_available_port(cls):
        cls.Lock.acquire()
        try:
            ports_in_use = cls.__get_ports_in_use()
            available_ports = cls.OpenPort - ports_in_use
            if available_ports:
                return random.choice(list(available_ports))
            else:
                raise PortExhaustionError(ErrorMsg.get_error_message(32))
        except Exception:
            raise
        finally:
            cls.Lock.release()

    @staticmethod
    def __get_ports_in_use() -> set:
        port_list: list = DockerPort.query.with_entities(DockerPort.port).all()
        return set([x[0] for x in port_list])

    @classmethod
    def add_unavailable_port(cls, port: int):
        cls.OpenPort = cls.OpenPort - {port, }
