#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/4 15:36
# @Author : wangweimin
# @File   : r_project_model.py
# @Desc   :

from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.project_operator.project_model_operator import ProjectModelService


ProjectModelGet = reqparse.RequestParser()
ProjectModelGet.add_argument('model_status_id', type=int, required=True, location='args')


class ProjectModel(Resource):

    @error_handler
    def get(self, project_id: str):
        """
        获取工程及其下模型信息
        ---
        tags:
          - 工程
        parameters:
          - name: project_id
            in: path
            type: integer
            required: true
          - name: model_status_id
            in: query
            type: integer
            default: 0
            required: true
            description: 模型过滤，若不过滤，传递0，其余参数对应为 1(生成失败), 2(生成成功), 3(正在生成), 5(打包成功), 6(打包失败), 7(正在打包)
        responses:
          500:
            description: 获取失败
            schema:
              properties:
                message:
                  items:
                    - name: Error
                      type: string
                code:
                  type: integer
            examples:
              {'message': {'ValueError': 'Error project id'}, 'code': 1}
          200:
            schema:
              properties:
                project_id:
                  type: integer
                code:
                  type: integer
                data:
                  type: array
                  items:
                    - name: model_id
                      type: integer
                    - name: model_name
                      type: string
                    - name: status
                      type: string
                    - name: create_time
                      type: string
                    - name: creator
                      type: string
                    - name: model_status_id
                      type: integer
            examples:
              {'code': 0, 'project_id': 1, 'data': [{'model_id': 1, 'model_name': 'model', 'status': '运行成功', 'create_time': '2019-01-01 00:00:00', 'creator': 'm', 'description': '说明', 'model_status_id': 1}, ]}
        """
        args = ProjectModelGet.parse_args()
        model_status_id = args['model_status_id'] or 0
        project_id = str2int(project_id)
        data = ProjectModelService.info(project_id=project_id, model_status_id=model_status_id)
        return jsonify(Response.correct(project_id=project_id, data=data))
