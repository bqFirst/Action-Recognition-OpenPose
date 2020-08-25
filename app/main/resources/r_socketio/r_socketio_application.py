#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/23 16:38
# @Author : wangweimin
# @File   : r_socketio_application.py
# @Desc   :

from flask import jsonify
from flask_restful import Resource

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.socketio_operator.application_socketio_operator import ApplicationSocketIOService


class ApplicationSocketIORefresh(Resource):

    @error_handler
    def put(self, application_id: str):
        application_id = str2int(application_id)
        ApplicationSocketIOService.refresh(application_id=application_id, address='application')
        return jsonify(Response.correct())
