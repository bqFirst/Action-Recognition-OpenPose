#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/29 16:49
# @Author : wangweimin
# @File   : r_application_model.py
# @Desc   :

from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.application_operator.application_model_operator import ApplicationModelService
from app.main.services.operator.application_operator.application_operator import ApplicationService

ApplicationModelGet = reqparse.RequestParser()
ApplicationModelGet.add_argument('model_status_id', type=int, location='args')


class ApplicationModel(Resource):

    @error_handler
    def get(self, application_id: str):
        """
        获取应用及其下模型信息
        ---
        tags:
          - 应用模型
        parameters:
          - name: application_id
            in: path
            type: integer
            required: true
          - name: model_status_id
            in: query
            type: integer
            default: 0
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
                  default: 1
            examples:
              {'code': 1, 'message': {'ValueError': 'Error application id'}}
          200:
            schema:
              properties:
                application_id:
                  type: integer
                code:
                  type: integer
                  default: 0
                data:
                  type: array
                  items:
                    - name: model_id
                      type: integer
                    - name: model_name
                      type: string
                    - name: model_status_id
                      type: integer
                      description: 模型过滤，若不过滤，传递0，其余参数对应为 1(生成失败), 2(生成成功), 3(正在生成), 5(打包成功), 6(打包失败), 7(正在打包)
                    - name: api
                      type: string
                    - name: description
                      type: string
                    - name: project_name
                      type: string
            examples:
              {'code': 0, 'data': [{'model_status_id': 2,'model_id': 1, 'model_name': 't1', 'api': '....', 'description': 'sha', 'project_name': 'myProject'}, ]}
        """
        args = ApplicationModelGet.parse_args()
        model_status_id = args['model_status_id'] or 0
        application_id = str2int(application_id)
        data = ApplicationModelService.info(application_id=application_id, model_status_id=model_status_id)
        return jsonify(Response.correct(application_id=application_id, data=data))


# put和delete共用
ApplicationModelOperatorQuery = reqparse.RequestParser()
ApplicationModelOperatorQuery.add_argument('model_id', type=int, location='form', required=True, action='append')


class ApplicationModelOperator(Resource):

    @error_handler
    def put(self, application_id: str):
        """
        应用增加模型
        ---
        tags:
          - 应用模型
        parameters:
          - name: application_id
            in: path
            type: integer
            required: true
          - name: model_id
            in: formData
            type: array
            required: True
            description: 应用需要新增的模型id
            items:
              type: integer
        responses:
          500:
            description: 新增失败
            schema:
              properties:
                message:
                  items:
                    - name: Error
                      type: string
                code:
                  type: integer
                  default: 1
            examples:
              {'code': 1, 'message': {'ValueError': 'Error model id'}}
          200:
            schema:
              properties:
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0}
        """
        args = ApplicationModelOperatorQuery.parse_args()
        models_id: list = args['model_id']
        application_id = str2int(application_id)
        ApplicationService.add_model(application_id=application_id, models_id=models_id)
        return jsonify(Response.correct())

    @error_handler
    def delete(self, application_id: str):
        """
        应用删除模型
        ---
        tags:
          - 应用模型
        parameters:
          - name: application_id
            in: path
            type: integer
            required: true
          - name: model_id
            in: formData
            type: array
            required: True
            description: 应用需要删除的模型id
            items:
              type: integer
        responses:
          500:
            description: 删除失败
            schema:
              properties:
                message:
                  items:
                    - name: Error
                      type: string
                code:
                  type: integer
                  default: 1
            examples:
              {'code': 1, 'message': {'ValueError': 'Error model id'}}
          200:
            schema:
              properties:
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0}
        """
        args = ApplicationModelOperatorQuery.parse_args()
        models_id: list = args['model_id']
        application_id = str2int(application_id)
        ApplicationService.delete_model(application_id=application_id, models_id=models_id)
        return jsonify(Response.correct())

    @error_handler
    def unused_get(self, application_id: str):
        """
        应用新增模型时的可选模型
        ---
        tags:
          - 应用模型
        parameters:
          - name: application_id
            in: path
            type: integer
            required: true
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
                  default: 1
            examples:
              {'code': 1, 'message': {'ValueError': 'Error application id'}}
          200:
            schema:
              properties:
                data:
                  type: array
                  description: 工程信息
                  items:
                    - name: catalog_name
                      type: string
                    - name: catalog_id
                      type: integer
                    - name: create_time
                      type: integer
                    - name: type
                      type: string
                    - name: child
                      type: array
                      items:
                        - name: project_name
                          type: string
                        - name: project_id
                          type: integer
                        - name: type
                          type: string
                        - name: create_time
                          type: integer
                        - name: child
                          type: array
                          items:
                            - name: model_name
                              type: string
                            - name: model_id
                              type: integer
                            - name: create_time
                              type: integer
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'data': [{'catalog_id': 1, 'catalog_name': 'myCatalog', 'create_time': 1562316263, 'type': 'catalog', 'child': [{'project_name': 'myProject', 'project_id': 1, 'create_time': 1562383671, 'type': 'project', 'child': [{'model_id': 1, 'model_name': 'myModel', 'create_time': 15623721287, 'type': 'model'}]}]}]}
        """
        pass
