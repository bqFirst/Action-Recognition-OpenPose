#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/15 9:20
# @Author : wangweimin
# @File   : r_database.py
# @Desc   :


from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.resources.resources_config import PermitDatabaseType
from app.main.services.operator.database_operator.database_operator import DatabaseService, DatabasesService
from app.models import User

DATAbasePost = reqparse.RequestParser()
DATAbasePost.add_argument('name', required=True, type=str, location='form')
DATAbasePost.add_argument('host', required=True, type=str, location='form')
DATAbasePost.add_argument('port', required=True, type=str, location='form')
DATAbasePost.add_argument('user', required=True, type=str, location='form')
DATAbasePost.add_argument('password', required=True, type=str, location='form')
DATAbasePost.add_argument('database', required=True, type=str, location='form')
DATAbasePost.add_argument('database_type', required=True, type=str, location='form', choices=PermitDatabaseType)
DATAbasePost.add_argument('description', type=str, location='form')

DATAbasePut = reqparse.RequestParser()
DATAbasePut.add_argument('host', required=True, type=str, location='form')
DATAbasePut.add_argument('port', required=True, type=str, location='form')
DATAbasePut.add_argument('user', required=True, type=str, location='form')
DATAbasePut.add_argument('password', required=True, type=str, location='form')
DATAbasePut.add_argument('database', required=True, type=str, location='form')
DATAbasePut.add_argument('database_type', required=True, type=str, location='form', choices=PermitDatabaseType)

DATAbaseGet = reqparse.RequestParser()
DATAbaseGet.add_argument('database_type', required=True, type=str, location='args', choices=PermitDatabaseType)


class DATAbase(Resource):

    @error_handler
    def post(self):
        """
        新建数据库链接，仅保存，不进行链接测试
        ---
        tags:
          - 数据库链接
        parameters:
          - name: name
            in: formData
            type: string
            required: true
            description: 数据库名称
          - name: description
            in: formData
            type: string
            description: 暂不需要提交描述！
          - name: host
            in: formData
            type: string
            required: True
          - name: port
            in: formData
            type: string
            required: True
          - name: user
            in: formData
            type: string
            required: True
          - name: password
            in: formData
            type: string
            required: True
          - name: database
            in: formData
            type: string
            required: True
          - name: database_type
            in: formData
            type: string
            required: True
            description: 数据库类型，如MySQL
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
              {'message': {'ValueError': 'name repeated'}, 'code': 1}
          200:
            description: 创建成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                database_id:
                  type: integer
            examples:
              {'code': 0, 'database_id': 1}
        """
        args = DATAbasePost.parse_args()
        host = args['host']
        port = args['port']
        user = args['user']
        password = args['password']
        database = args['database']
        creator_id: int = User.query.first().id
        name = args['name']
        description = args['description'] or ''
        database_type = args['database_type']
        database_id: int = DatabaseService.create(host=host, port=port, user=user, password=password,
                                                  database=database, database_type=database_type, name=name,
                                                  description=description, creator_id=creator_id)
        return jsonify(Response.correct(database_id=database_id))

    @error_handler
    def put(self):
        """
        验证数据库链接
        ---
        tags:
          - 数据库链接
        parameters:
          - name: host
            in: formData
            type: string
            required: True
          - name: port
            in: formData
            type: string
            required: True
          - name: user
            in: formData
            type: string
            required: True
          - name: password
            in: formData
            type: string
            required: True
          - name: database
            in: formData
            type: string
            required: True
          - name: database_type
            in: formData
            type: string
            required: True
            description: 数据库类型，如MySQL
        responses:
          500:
            description: 验证失败
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
            description: 验证通过
            schema:
              properties:
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0}
        """
        args = DATAbasePut.parse_args()
        host = args['host']
        port = args['port']
        user = args['user']
        password = args['password']
        database = args['database']
        database_type = args['database_type']
        DatabaseService.verify(host=host, port=port, user=user, password=password, database=database,
                               database_type=database_type)
        return jsonify(Response.correct())

    @error_handler
    def get(self):
        """
        获取特定类型数据库链接信息
        ---
        tags:
          - 数据库链接
        parameters:
          - name: database_type
            in: query
            type: string
            required: True
            description: 数据库类型，如MySQL
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
              {'message': {'ValueError': 'name repeated'}, 'code': 1}
          200:
            description: 创建成功
            schema:
              properties:
                data:
                  type: array
                  items:
                    - name: database_id
                      type: string
                    - name: name
                      type: string
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'data': [{'database_id': 1, 'name': 'ramadb (MYSQL 127.0.0.1:3306)'}]}
        """
        args = DATAbaseGet.parse_args()
        database_type = args['database_type']
        creator_id: int = User.query.first().id
        result: list = DatabasesService.databases_info_by_type(database_type=database_type,
                                                               creator_id=creator_id)
        return jsonify(Response.correct(data=result))


DATAbaseOperatorPut = reqparse.RequestParser()
DATAbaseOperatorPut.add_argument('name', required=True, type=str, location='form')
DATAbaseOperatorPut.add_argument('host', required=True, type=str, location='form')
DATAbaseOperatorPut.add_argument('port', required=True, type=str, location='form')
DATAbaseOperatorPut.add_argument('user', required=True, type=str, location='form')
DATAbaseOperatorPut.add_argument('password', required=True, type=str, location='form')
DATAbaseOperatorPut.add_argument('database', required=True, type=str, location='form')
DATAbaseOperatorPut.add_argument('database_type', required=True, type=str, location='form', choices=PermitDatabaseType)
DATAbaseOperatorPut.add_argument('description', type=str, location='form')


class DATAbaseOperator(Resource):

    @error_handler
    def get(self, database_id: str):
        """
        获取数据库链接信息
        ---
        tags:
          - 数据库链接
        parameters:
          - name: database_id
            in: path
            type: integer
            required: True
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
              {'message': {'ValueError': 'error database id'}, 'code': 1}
          200:
            description: 获取成功
            schema:
              properties:
                name:
                  type: string
                host:
                  type: string
                port:
                  type: string
                user:
                  type: string
                password:
                  type: string
                database:
                  type: string
                database_id:
                  type: integer
                description:
                  type: string
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'name': 'test_db', 'host':'127.0.0.1', 'port':'3306', 'user':'m', 'password':'password', 'database':'db', 'database_id': 1, 'description': 'nothing'}
        """
        creator_id: int = User.query.first().id
        database_id = str2int(database_id)
        result: dict = DatabaseService.info(database_id=database_id, creator_id=creator_id)
        return jsonify(Response.correct(**result))

    @error_handler
    def put(self, database_id: str):
        """
        修改数据库链接信息，仅保存，不进行链接测试
        ---
        tags:
          - 数据库链接
        parameters:
          - name: database_id
            in: path
            type: integer
            required: True
          - name: name
            in: formData
            type: string
            required: true
            description: 数据库名称
          - name: description
            in: formData
            type: string
            description: 暂不需要提交描述！
          - name: host
            in: formData
            type: string
            required: True
          - name: port
            in: formData
            type: string
            required: True
          - name: user
            in: formData
            type: string
            required: True
          - name: password
            in: formData
            type: string
            required: True
          - name: database
            in: formData
            type: string
            required: True
          - name: database_type
            in: formData
            type: string
            required: True
            description: 数据库类型，如MySQL
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
              {'message': {'ValueError': 'name repeated'}, 'code': 1}
          200:
            description: 创建成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0}
        """
        args = DATAbaseOperatorPut.parse_args()
        host = args['host']
        port = args['port']
        user = args['user']
        password = args['password']
        database = args['database']
        creator_id: int = User.query.first().id
        name = args['name']
        description = args['description'] or ''
        database_type = args['database_type']
        database_id = str2int(database_id)
        DatabaseService.modify(host=host, port=port, user=user, password=password, database=database,
                               database_type=database_type, name=name, description=description,
                               creator_id=creator_id, database_id=database_id)
        return jsonify(Response.correct())

    @error_handler
    def delete(self, database_id: str):
        """
        删除数据库链接
        ---
        tags:
          - 数据库链接
        parameters:
          - name: database_id
            in: path
            type: integer
            required: True
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
              {'message': {'ValueError': 'error database id'}, 'code': 1}
          200:
            description: 创建成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                  description: 0表示操作成功，5表示无法删除，有数据库数据使用该源
                data:
                  type: array
                  items:
                    type: string
            examples:
              {'code': 5, 'data': ['工程1-数据1', '工程2-数据2']}
        """
        creator_id: int = User.query.first().id
        database_id = str2int(database_id)
        result: list = DatabaseService.delete(database_id=database_id, creator_id=creator_id)
        if result:
            return jsonify(Response.delete_refused(data=result))
        return jsonify(Response.correct())


class DATABASEUsed(Resource):

    @error_handler
    def get(self, database_id: str):
        """
        获取数据库链接被使用情况
        ---
        tags:
          - 数据库链接
        parameters:
          - name: database_id
            in: path
            type: integer
            required: True
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
              {'message': {'ValueError': 'error database id'}, 'code': 1}
          200:
            description: 获取成功
            schema:
              properties:
                data:
                  type: array
                  items:
                    - name: project_name
                      type: string
                    - name: data_name
                      type: string
                    - name: application_name
                      type: string
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'data': [{'project_name': 'project', 'data_name': 'xxx'}, {'application_name': 'app', 'data_name': 'xxx'}]}
        """
        creator_id: int = User.query.first().id
        database_id = str2int(database_id)
        result: dict = DatabaseService.used(database_id=database_id, creator_id=creator_id)
        return jsonify(Response.correct(data=result))
