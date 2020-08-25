#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/1/21 17:28
# @Author : wangweimin
# @File   : r_case.py
# @Desc   :

from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.case_operator.case_operator import CaseService
from app.models import User

CASEPost = reqparse.RequestParser()
CASEPost.add_argument('short_id', required=True, type=str, location='form')
CASEPost.add_argument('port', required=True, type=int, location='form')
CASEPost.add_argument('case_name', required=True, type=str, location='form')
CASEPost.add_argument('catalog_id', required=True, type=int, location='form')


class CASE(Resource):

    @error_handler
    def post(self):
        """
        新建案例，docker容器必须处于启动状态！
        ---
        tags:
          - 案例
        parameters:
          - name: short_id
            in: formData
            type: string
            required: true
            description: 容器short id
          - name: port
            in: formData
            type: integer
            required: true
            description: 容器开放的端口被映射的端口
          - name: case_name
            in: formData
            type: string
            description: 案例名称
          - name: catalog_id
            in: formData
            type: integer
            description: 案例目录id
        responses:
          500:
            description: 创建失败
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
              {'code': 1, 'message': {'ValueError': 'name repeated'}}
          200:
            description: 创建成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                case_id:
                  type: integer
            examples:
              {'code': 0, 'case_id': 1}
        """
        args = CASEPost.parse_args()
        short_id = args['short_id']
        port = args['port']
        case_name = args['case_name']
        catalog_id = args['catalog_id']
        user_id = User.query.first().id
        case_id = CaseService.create(short_id=short_id, port=port, case_name=case_name, user_id=user_id,
                                     catalog_id=catalog_id)
        return jsonify(Response.correct(case_id=case_id))


CASEOperatorPut = reqparse.RequestParser()
CASEOperatorPut.add_argument('case_name', required=True, type=str, location='form')
CASEOperatorPut.add_argument('description', required=True, type=str, location='form')
CASEOperatorPut.add_argument('scene', required=True, type=str, location='form')
CASEOperatorPut.add_argument('data_trained', required=True, type=str, location='form')
CASEOperatorPut.add_argument('data_treatment', required=True, type=str, location='form')
CASEOperatorPut.add_argument('model_algorithm', required=True, type=str, location='form')
CASEOperatorPut.add_argument('model_trained', required=True, type=str, location='form')


class CASEOperator(Resource):

    @error_handler
    def put(self, case_id: str):
        """
        修改案例名称或描述信息
        ---
        tags:
          - 案例
        parameters:
          - name: case_id
            in: path
            type: integer
            required: true
            description: 案例id
          - name: case_name
            in: formData
            required: true
            type: string
          - name: description
            in: formData
            required: true
            type: string
          - name: scene
            in: formData
            type: string
            required: true
          - name: data_trained
            in: formData
            type: string
            required: true
          - name: data_treatment
            in: formData
            type: string
            required: true
          - name: model_algorithm
            in: formData
            type: string
            required: true
          - name: model_trained
            in: formData
            type: string
            required: true
        responses:
          500:
            description: 修改失败
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
              {'code': 1, 'message': {'ValueError': 'Error case id'}}
          200:
            description: 修改成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0}
        """
        case_id = str2int(case_id)
        args = CASEOperatorPut.parse_args()
        case_name = args['case_name']
        description = args['description']
        scene = args['scene']
        data_trained = args['data_trained']
        data_treatment = args['data_treatment']
        model_algorithm = args['model_algorithm']
        model_trained = args['model_trained']

        CaseService.modify(case_id=case_id, case_name=case_name, description=description, scene=scene,
                           data_trained=data_trained, data_treatment=data_treatment, model_algorithm=model_algorithm,
                           model_trained=model_trained)

        return jsonify(Response.correct())

    @error_handler
    def delete(self, case_id: str):
        """
        删除案例
        ---
        tags:
          - 案例
        parameters:
          - name: case_id
            in: path
            type: integer
            required: true
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
              {'code': 1, 'message': {'ValueError': 'Error case id'}}
          200:
            description: 删除成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0}
        """
        case_id = str2int(case_id)
        CaseService.delete(case_id=case_id)
        return jsonify(Response.correct())

    @error_handler
    def get(self, case_id):
        """
        获取案例信息
        ---
        tags:
          - 案例
        parameters:
          - name: case_id
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
              {'code': 1, 'message': {'ValueError': 'Error case id'}}
          200:
            description: 案例信息
            schema:
              properties:
                data:
                  type: array
                  items:
                    - name: case_id
                      type: integer
                    - name: case_name
                      type: string
                    - name: description
                      type: string
                    - name: scene
                      type: string
                    - name: data_trained
                      type: string
                    - name: data_treatment
                      type: string
                    - name: model_algorithm
                      type: string
                    - name: model_trained
                      type: string
                    - name: model_assessment
                      type: array
                      items:
                        - name: attribute
                          type: string
                        - name: value
                          type: string
                    - name: param
                      type: array
                      items:
                        - name: mode_name
                          type: string
                        - name: mode_id
                          type: integer
                        - name: input
                          type: array
                          items:
                            - name: param_name
                              type: string
                            - name: param_type
                              type: string
                            - name: param_type_id
                              type: integer
                        - name: output
                          type: array
                          items:
                            - name: param_name
                              type: string
                            - name: param_type
                              type: string
                            - name: param_type_id
                              type: integer
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'data': {'case_id': 1, 'case_name': '人体识别', 'case_description': '关键点识别', 'case_scene': '人员入侵等', 'model_assessment': [{'attribute':'精确度', 'value': '87%'}], 'param': [{'mode_name':'图片识别', 'mode_id': 1, 'input':[{'param_name': 'picture', 'param_type':'picyure', 'param_type_id':1}], 'output':[{'param_name': 'picture', 'param_type':'picyure', 'param_type_id':1}, {'param_name': 'body_json', 'param_type':'json', 'param_type_id':3}]},{'mode_name':'视频识别', 'input':[{'param_name': 'video', 'param_type':'video', 'param_type_id':2}], 'output':[{'param_name': 'video', 'param_type':'video', 'param_type_id':2}]}]}}
        """
        case_id = str2int(case_id)
        data = CaseService.get(case_id=case_id)
        return jsonify(Response.correct(data=data))
