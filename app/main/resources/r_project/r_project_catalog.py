#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/2 17:33
# @Author : wangweimin
# @File   : r_project_catalog.py
# @Desc   :


from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.project_operator.project_catalog_operator import ProjectCatalogService
from app.models import User

PROJECTCatalogPost = reqparse.RequestParser()
PROJECTCatalogPost.add_argument('catalog_pid', type=int, location='form', required=True)
PROJECTCatalogPost.add_argument('catalog_name', type=str, location='form', required=True)


class PROJECTCatalog(Resource):

    @error_handler
    def get(self):
        """
        获取工程目录结构
        ---
        tags:
          - 工程目录
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
              {'message': {'Error': 'Error'}, 'code': 1}
          200:
            description: 工程目录层级结构
            schema:
              properties:
                data:
                  type: array
                  description: 工程目录层级
                  items:
                    type: dict
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'data': [{'create_time':1572417880, 'type': 'catalog', 'name': '默认目录', 'child':[{'type': 'project', 'project_id': 1, 'name':'myProject', 'create_time': '2910-01-01 00:00:00'}, {'type': 'project', 'project_id': 2, 'name':'myProject2', 'create_time': '2910-01-01 00:00:00'}, {'create_time':1572417880, 'type': 'catalog', 'catalog_id': 2, 'name':'我的目录', 'child': []}], 'catalog_id': 1}, {'create_time':1572417880, 'name': '目录', 'catalog_id': 3, 'type':'catalog', 'child':[]}]}
        """
        tree = ProjectCatalogService.tree(catalog_id=0)
        return jsonify(Response.correct(data=tree))

    @error_handler
    def post(self):
        """
        新建工程目录
        ---
        tags:
          - 工程目录
        parameters:
          - name: catalog_name
            in: formData
            type: string
            required: true
            description: 新建目录名称
          - name: catalog_pid
            in: formData
            type: integer
            required: true
            default: 0
            description: 父级目录id，若为根级则为0
        responses:
          500:
            description: 新建失败
            schema:
              properties:
                code:
                  type: integer
                  default: 1
                message:
                  items:
                    - name: Error
                      type: string
            examples:
              {'message': {'ValueError': 'name repeated'}, 'code': 1}
          200:
            description: 新建成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                catalog_id:
                  type: integer
            examples:
              {'code': 0, 'catalog_id': 1}
        """
        args = PROJECTCatalogPost.parse_args()
        catalog_pid = args['catalog_pid']
        catalog_name = args['catalog_name']
        user_id = User.query.first().id
        catalog_id: int = ProjectCatalogService.create(catalog_name=catalog_name, catalog_pid=catalog_pid,
                                                       user_id=user_id)
        return jsonify(Response.correct(catalog_id=catalog_id))


PROJECTCatalogOperatorPut = reqparse.RequestParser()
PROJECTCatalogOperatorPut.add_argument('catalog_name', required=True, type=str, location='form')


class PROJECTCatalogOperator(Resource):

    @error_handler
    def delete(self, catalog_id: str):
        """
        删除工程目录
        ---
        tags:
          - 工程目录
        parameters:
          - name: catalog_id
            in: path
            type: integer
            required: true
            description: 目录id
        responses:
          500:
            description: 删除失败
            schema:
              properties:
                message:
                  description: 失败原因
                  items:
                    - name: Error
                      type: string
                code:
                  type: integer
                  default: 1
            examples:
              {'message': {'ValueError': 'project in such catalog'}, 'code': 1}
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
        catalog_id = str2int(catalog_id)
        ProjectCatalogService.delete(catalog_id=catalog_id)
        return jsonify(Response.correct())

    @error_handler
    def put(self, catalog_id: str):
        """
        修改工程目录名称
        ---
        tags:
          - 工程目录
        parameters:
          - name: catalog_id
            in: path
            type: integer
            required: true
            description: 目录id
          - name: catalog_name
            in: formData
            type: string
            required: true
            description: 新的目录名称
        responses:
          500:
            description: 修改失败
            schema:
              properties:
                message:
                  description: 失败原因
                  items:
                    - name: Error
                      type: string
                code:
                  type: integer
                  default: 1
            examples:
              {'message': {'ValueError': 'name repeated'}, 'code': 1}
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
        args = PROJECTCatalogOperatorPut.parse_args()
        catalog_name = args['catalog_name']
        catalog_id = str2int(catalog_id)
        ProjectCatalogService.rename(catalog_name=catalog_name, catalog_id=catalog_id)
        return jsonify(Response.correct())

    @error_handler
    def get(self, catalog_id: str):
        """
        获取工程目录信息
        ---
        tags:
          - 工程目录
        parameters:
          - name: catalog_id
            in: path
            type: integer
            required: true
        responses:
          500:
            description: 获取失败
            schema:
              properties:
                message:
                  description: 失败原因
                  items:
                    - name: Error
                      type: string
                code:
                  type: integer
                  default: 1
            examples:
              {'message': {'ValueError': 'Error catalog id'}, 'code': 1}
          200:
            description: 获取成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                catalog_name:
                  type: string
                catalog_id:
                  type: integer
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'catalog_name': 'catalog', 'catalog_id': 1}
        """
        catalog_id = str2int(catalog_id)
        result = ProjectCatalogService.get(catalog_id=catalog_id)
        return jsonify(Response.correct(**result))


class PROJECTCatalogProject(Resource):

    @error_handler
    def get(self, catalog_id: str):
        """
        获取工程目录下工程信息
        ---
        tags:
          - 工程目录
        parameters:
          - name: catalog_id
            in: path
            type: integer
            required: true
            description: 目录id，若catalog_id为0，则获取所有工程信息
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
              {'message': {'ValueError': 'Error catalog id'}, 'code': 1}
          200:
            description: 获取成功
            schema:
              properties:
                data:
                  type: array
                  description: 工程信息
                  items:
                    type: dict
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'data': [{'project_id': 1, 'project_name': 'myProject', 'creator': 'me', 'create_time': '2019-01-01: 00:00:00'}]}
        """
        catalog_id = str2int(catalog_id)
        data = ProjectCatalogService.project_info(catalog_id=catalog_id)
        return jsonify(Response.correct(data=data))


PROJECTCatalogModelGet = reqparse.RequestParser()
PROJECTCatalogModelGet.add_argument('catalog_id', type=int, required=True, location='args')
PROJECTCatalogModelGet.add_argument('models_id', type=int, location='args', action='append')


class PROJECTCatalogModel(Resource):

    @error_handler
    def get(self):
        """
        获取工程目录下模型信息（已训练好的模型）
        ---
        tags:
          - 工程目录
        parameters:
          - name: catalog_id
            in: query
            type: integer
            required: true
            description: 目录id，若catalog_id为0，则获取所有工程信息
          - name: models_id
            in: query
            type: array
            items:
              type: integer
            description: 在应用新增模型需要展示模型列表时使用，传递需要忽略的模型id
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
              {'message': {'ValueError': 'Error catalog id'}, 'code': 1}
          200:
            description: 获取成功
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
                            - name: type
                              type: string
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'data': [{'catalog_id': 1, 'catalog_name': 'myCatalog', 'create_time': 1562316263, 'type': 'catalog', 'child': [{'project_name': 'myProject', 'project_id': 1, 'create_time': 1562383671, 'type': 'project', 'child': [{'model_id': 1, 'model_name': 'myModel', 'create_time': 15623721287, 'type': 'model'}]}]}]}
        """
        args = PROJECTCatalogModelGet.parse_args()
        catalog_id = args['catalog_id'] or 0
        models_id = args['models_id'] or []
        user_id = User.query.first().id
        result = ProjectCatalogService.model_tree(catalog_id=catalog_id, user_id=user_id, models_id=models_id)
        return jsonify(Response.correct(data=result))
