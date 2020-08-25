#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/2/11 15:22
# @Author : wangweimin
# @File   : docker_container_request_operator.py
# @Desc   :

import requests

from app.main.basic_main.custom_error import DockerContainerPredictError
from app.models import DockerContainer


class DockerContainerRequestService(object):

    PredictUrl: str = 'http://{}:{}/predict'

    @classmethod
    def post_predict(cls, docker_container: DockerContainer, form_data: dict) -> dict:
        port: int = docker_container.port
        url: str = cls.PredictUrl.format('127.0.0.1', port)
        response = requests.post(url, data=form_data)
        result: dict = response.json()
        if not result['code']:
            return result
        raise DockerContainerPredictError(result.get('message').get('Error'))
