#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/23 15:25
# @Author : wangweimin
# @File   : r_socketio_project.py
# @Desc   :


from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.socketio_operator.project_socketio_operator import ProjectSocketIOService

ProjectSocketIORefreshPut = reqparse.RequestParser()
ProjectSocketIORefreshPut.add_argument('address', required=True, type=str, location='form')


class ProjectSocketIORefresh(Resource):

    @error_handler
    def put(self, project_id: str):
        project_id = str2int(project_id)
        args = ProjectSocketIORefreshPut.parse_args()
        address = args['address']
        ProjectSocketIOService.refresh(project_id=project_id, address=address)
        return jsonify(Response.correct())
