#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/2 11:27
# @Author : wangweimin
# @File   : r_data_source_catalog.py
# @Desc   :


from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.catalog_operator import data_source_tree
from app.main.services.operator.data_source_operator import catalog_data_link_info
from app.main.services.operator.data_source_catalog_operator.data_source_catalog_operator import \
    ds_catalog_create_service, ds_catalog_delete_service, ds_catalog_modify_service
from app.models import DataSourceCatalog, User

DSCatalogPost = reqparse.RequestParser()
DSCatalogPost.add_argument('catalog_pid', type=int, location='form', required=True)
DSCatalogPost.add_argument('catalog_name', type=str, location='form', required=True)


class DSCatalog(Resource):

    @error_handler
    def get(self):
        """
        获取数据源目录结构
        ---
        tags:
          - 数据源目录
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
              {'message': {'Error': 'Connect database failed'}, 'code': 1}
          200:
            description: 数据源目录层级结构
            schema:
              properties:
                data:
                  type: array
                  description: 数据源目录层级
                  items:
                    type: dict
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'data': [{'type': 'catalog', 'name': '默认目录', 'child':[{'type': 'data', 'data_link_id': 1, 'name':'data.csv'}, {'type': 'data', 'data_link_id': 2, 'name':'data2.csv'}, {'type': 'catalog', 'catalog_id': 2, 'name':'我的目录', 'child': []}], 'catalog_id': 1}, {'name': '目录', 'catalog_id': 3, 'type':'catalog', 'child':[]}]}
        """
        tree = data_source_tree(catalog_id=0)
        res = Response.correct()
        res.update(data=tree)
        return jsonify(res)

    @error_handler
    def post(self):
        """
        新建数据源目录
        ---
        tags:
          - 数据源目录
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
            description: 新建成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0}
        """
        args = DSCatalogPost.parse_args()
        catalog_pid = args['catalog_pid']
        catalog_name = args['catalog_name']
        user_id = User.query.first().id
        ds_catalog_create_service(catalog_name=catalog_name, user_id=user_id, catalog_pid=catalog_pid)
        return jsonify(Response.correct())


DSCatalogOperatorPut = reqparse.RequestParser()
DSCatalogOperatorPut.add_argument('catalog_name', required=True, type=str, location='form')


class DSCatalogOperator(Resource):

    @error_handler
    def delete(self, catalog_id: str):
        """
        删除目录
        ---
        tags:
          - 数据源目录
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
              {'message': {'ValueError': 'data link in such catalog'}, 'code': 1}
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
        if 1 == catalog_id:
            return jsonify(Response.error(message={'Error': "无法删除"}))
        ds_catalog_delete_service(catalog_id=catalog_id)
        return jsonify(Response.correct())

    @error_handler
    def put(self, catalog_id: str):
        """
        修改目录名称
        ---
        tags:
          - 数据源目录
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
        args = DSCatalogOperatorPut.parse_args()
        catalog_name = args['catalog_name']
        catalog_id = str2int(catalog_id)
        ds_catalog_modify_service(catalog_name=catalog_name, catalog_id=catalog_id)
        return jsonify(Response.correct())

    @error_handler
    def get(self, catalog_id: str):
        """
        获取数据源目录信息
        ---
        tags:
          - 数据源目录
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
                code:
                  type: integer
                  default: 0
            examples:
              {'catalog_name': 'ds', 'catalog_id': 1, 'code': 0}
        """
        catalog_id = str2int(catalog_id)
        data_source_catalog: DataSourceCatalog = DataSourceCatalog.query.get(catalog_id)
        if not data_source_catalog:
            raise ValueError('Error catalog id')
        else:
            return jsonify(Response.correct(catalog_id=catalog_id, catalog_name=data_source_catalog.name))


class DSCatalogData(Resource):

    @error_handler
    def get(self, catalog_id: str):
        """
        获取数据源目录下数据链接信息
        ---
        tags:
          - 数据源目录
        parameters:
          - name: catalog_id
            in: path
            type: integer
            required: true
            description: 目录id，若id为0，则获取所有数据信息
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
                    type: dict
                code:
                  type: integer
                  default: 0
            examples:
              data: [{'data_link_id': 1, 'data_name': 'data.csv', 'creator': 'me', 'create_time': '2019-01-01: 00:00:00', 'data_link_type': 'file'}]
        """
        catalog_id = str2int(catalog_id)
        data = catalog_data_link_info(catalog_id=catalog_id)
        return jsonify(Response.correct(data=data))
