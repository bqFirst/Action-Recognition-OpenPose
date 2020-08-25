#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/3 10:49
# @Author : wangweimin
# @File   : r_application_catalog.py
# @Desc   :


from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.application_operator.application_catalog_operator import ApplicationCatalogService
from app.models import User

APPLICATIONCatalogPost = reqparse.RequestParser()
APPLICATIONCatalogPost.add_argument('catalog_pid', type=int, location='form', required=True)
APPLICATIONCatalogPost.add_argument('catalog_name', type=str, location='form', required=True)


class APPLICATIONCatalog(Resource):

    @error_handler
    def get(self):
        """
        获取应用目录结构
        ---
        tags:
          - 应用目录
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
              {'message': {'Error': 'Get data error'}, 'code': 1}
          200:
            description: 应用目录层级结构
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
              {'code': 0, 'data': [{'type': 'catalog', 'name': '默认目录', 'child':[{'type': 'application', 'application_id': 1, 'name':'app1', 'create_time': 13214241241}, {'type': 'catalog', 'catalog_id': 2, 'name':'我的目录', 'child': []}], 'catalog_id': 1}, {'name': '目录', 'catalog_id': 3, 'type':'catalog', 'child':[]}]}
        """
        tree = ApplicationCatalogService.tree(catalog_id=0)
        return jsonify(Response.correct(data=tree))

    @error_handler
    def post(self):
        """
        新建应用目录
        ---
        tags:
          - 应用目录
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
              {'code': 1, 'message': {'ValueError': 'name repeated'}}
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
        args = APPLICATIONCatalogPost.parse_args()
        catalog_name = args['catalog_name']
        catalog_pid = args['catalog_pid']
        user_id = User.query.first().id
        catalog_id = ApplicationCatalogService.create(catalog_name=catalog_name, catalog_pid=catalog_pid, user_id=user_id)
        return jsonify(Response.correct(catalog_id=catalog_id))


APPLICATIONCatalogOperatorPut = reqparse.RequestParser()
APPLICATIONCatalogOperatorPut.add_argument('catalog_name', type=str, required=True, location='form')


class APPLICATIONCatalogOperator(Resource):

    @error_handler
    def delete(self, catalog_id: str):
        """
        删除应用目录
        ---
        tags:
          - 应用目录
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
                  items:
                    - name: Error
                      type: string
                code:
                  type: integer
                  default: 1
            examples:
              {'message': {'Error': 'there are applications in such catalog'}, 'code': 1}
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
        ApplicationCatalogService.delete(catalog_id=catalog_id)
        return jsonify(Response.correct())

    @error_handler
    def put(self, catalog_id: str):
        """
        修改应用目录名称
        ---
        tags:
          - 应用目录
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
        catalog_id = str2int(catalog_id)
        args = APPLICATIONCatalogOperatorPut.parse_args()
        catalog_name = args['catalog_name']
        ApplicationCatalogService.rename(catalog_id=catalog_id, catalog_name=catalog_name)
        return jsonify(Response.correct())

    @error_handler
    def unused_get(self, catalog_id: str):
        """
        获取应用目录信息
        ---
        tags:
          - 应用目录
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
                  items:
                    - name: Error
                      type: string
                code:
                  type: integer
                  default: 1
            examples:
              {'message': {'ValueError': 'Error catalog id'}, 'code': 1}
          200:
            schema:
              properties:
                catalog_name:
                  type: string
                catalog_id:
                  type: integer
            examples:
              {'code': 0, 'catalog_name': 'catalog', 'catalog_id': 1}
        """
        pass


class APPLICATIONCatalogApplication(Resource):

    @error_handler
    def get(self, catalog_id: str):
        """
        获取应用目录下应用信息
        ---
        tags:
          - 应用目录
        parameters:
          - name: catalog_id
            in: path
            type: integer
            required: true
            description: 目录id，若id为0，则获取所有应用信息
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
                  description: 数据链接信息
                  items:
                    - name: application_id
                      type: integer
                    - name: application_name
                      type: string
                    - name: creator
                      type: string
                    - name: create_time
                      type: string
                    - name: status_name
                      type: string
                    - name: status_id
                      type: integer
                    - name: image_status_id
                      type: integer
                      description: 1未打包，2打包中，3打包成功
                    - name: image_status_name
                      type: string
                code:
                  type: integer
                  default: 0
            examples:
              {'data': [{'image_status_id': '未打包', 'image_status_id': 1, 'application_id': 1, 'application_name': 'app1', 'creator': 'me', 'create_time': '2019-01-01: 00:00:00', 'status_name': '服务中', 'status_id': 1}], 'code': 0}
        """
        catalog_id = str2int(catalog_id)
        user_id = User.query.first().id
        data = ApplicationCatalogService.application_info(catalog_id=catalog_id, user_id=user_id)
        return jsonify(Response.correct(data=data))
