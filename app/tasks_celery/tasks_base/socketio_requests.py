#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/23 16:05
# @Author : wangweimin
# @File   : socketio_requests.py
# @Desc   :

import requests

from conf.system_config import ServerAddress


class SocketIORequestsService(object):

    @staticmethod
    def refresh_project(project_id: int, address: str):
        requests.put('http://{}/socketio/project/{}'.format(ServerAddress.get_address(), project_id),
                     data={'address': address})

    @staticmethod
    def refresh_application(application_id: int):
        requests.put('http://{}/socketio/app/{}'.format(ServerAddress.get_address(), application_id),
                     data={'address': 'application'})
