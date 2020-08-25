#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/15 10:03
# @Author : wangweimin
# @File   : r_database_data.py
# @Desc   :

import math
import pandas as pd

from flask_restful import Resource, reqparse
from flask import jsonify

# from app.main.resources.resources_config import PermitDatabaseType
from app.main.basic_main.custom_error import RequestValueError
from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_param_judgement import one_and_the_only
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.resources.resources_config import PermitAscriptionType
from app.main.services.operator.database_operator.application_database_data_operator import AppDatabaseDataService
from app.main.services.operator.database_operator.project_database_data_operator import ProDatabaseDataService
from app.main.services.operator.database_operator.database_idata_operator import DatabaseSQLService, DatabaseDataService
from app.models import User

DatabaseDataPost = reqparse.RequestParser()
DatabaseDataPost.add_argument('sql', required=True, type=str, location='form')
DatabaseDataPost.add_argument('data_name', required=True, type=str, location='form')
DatabaseDataPost.add_argument('database_id', required=True, type=int, location='form')
DatabaseDataPost.add_argument('project_id', type=str, location='form')
DatabaseDataPost.add_argument('application_id', type=str, location='form')
DatabaseDataPost.add_argument('data_link_id', type=int, location='form')

DatabaseDataPut = reqparse.RequestParser()
DatabaseDataPut.add_argument('sql', required=True, type=str, location='form')
DatabaseDataPut.add_argument('database_id', required=True, type=int, location='form')
DatabaseDataPut.add_argument('limit', type=int, location='form')


class DATABASEData(Resource):

    @error_handler
    def post(self):
        """
        查询数据库形成文件数据 / 编辑数据库数据
        ---
        tags:
          - 数据库数据
        parameters:
          - name: database_id
            in: formData
            type: integer
            required: True
          - name: project_id
            in: formData
            type: integer
            description: 若为应用数据，不传递该参数
          - name: application_id
            in: formData
            type: integer
            description: 若为工程原始数据，不传递该参数
          - name: sql
            in: formData
            type: string
            required: true
            description: 查询语句
          - name: data_name
            in: formData
            type: string
            required: True
            description: 创建的数据文件名称
          - name: data_link_id
            in: formData
            type: integer
            description: 在编辑数据库数据时使用，以用来替换原有数据
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
        args = DatabaseDataPost.parse_args()
        sql = args['sql']
        data_name = args['data_name']
        database_id = args['database_id']
        project_id = args['project_id'] or None
        application_id = args['application_id'] or None
        one_and_the_only(project_id, application_id)
        data_link_id = args['data_link_id']
        creator_id: int = User.query.first().id
        if project_id:
            if data_link_id is None:
                database_data_id = ProDatabaseDataService.create(sql=sql, data_name=data_name, database_id=database_id,
                                                                 project_id=project_id, creator_id=creator_id)
            else:
                database_data_id = ProDatabaseDataService.edit(sql=sql, data_name=data_name, database_id=database_id,
                                                               project_id=project_id, creator_id=creator_id,
                                                               data_link_id=data_link_id)
        else:
            if data_link_id is None:
                database_data_id = AppDatabaseDataService.create(sql=sql, data_name=data_name, database_id=database_id,
                                                                 application_id=application_id, creator_id=creator_id)
            else:
                database_data_id = AppDatabaseDataService.edit(sql=sql, data_name=data_name, database_id=database_id,
                                                               application_id=application_id, creator_id=creator_id,
                                                               data_link_id=data_link_id)
        return jsonify(Response.correct(database_data_id=database_data_id))

    @error_handler
    def put(self):
        """
        验证数据库查询语句
        ---
        tags:
          - 数据库数据
        parameters:
          - name: database_id
            in: formData
            type: integer
            required: True
          - name: sql
            in: formData
            type: string
            required: true
            description: 查询语句
          - name: limit
            in: formData
            type: integer
            description: 显示的数据条数，默认为100
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
              {'message': {'Error': 'failure reason'}, 'code': 1}
          200:
            description: 验证成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                data:
                  type: array
                  description: 数据链接数据
                  items:
                   - name: a
                     type: integer
                   - name: b
                     type: integer
            examples:
              {'code': 0, 'data' : [{'a':1, 'b':2}, {'a': 2, 'b': 3}]}
        """
        args = DatabaseDataPut.parse_args()
        sql = args['sql']
        limit = args['limit'] or 100
        database_id = args['database_id']
        creator_id: int = User.query.first().id
        data: pd.DataFrame = DatabaseSQLService.select(database_id=database_id, sql=sql, creator_id=creator_id)
        result_data: pd.DataFrame = data[:limit]
        return jsonify(Response.correct(data=result_data.to_dict(orient='record')))


DatabaseDataOperatorPut = reqparse.RequestParser()
DatabaseDataOperatorPut.add_argument('data_name', required=True, type=str, location='form')
DatabaseDataOperatorPut.add_argument('ascription', type=str, location='form', choices=PermitAscriptionType)

DatabaseDataOperatorDelete = reqparse.RequestParser()
DatabaseDataOperatorDelete.add_argument('is_forced', type=int, location='form', choices=(0, 1))
DatabaseDataOperatorDelete.add_argument('ascription', type=str, location='form', choices=PermitAscriptionType)


class DatabaseDataOperator(Resource):

    @error_handler
    def get(self, data_link_id: str):
        """
        获取数据库数据的信息
        ---
        tags:
          - 数据库数据
        parameters:
          - name: data_link_id
            in: path
            type: integer
            required: true
            description: 数据链接id
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
              {'code': 1, 'message': {'ValueError': 'Error data link id'}}
          200:
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                data:
                  items:
                    - name: data_link_id
                      type: integer
                    - name: data_name
                      type: string
                    - name: database_id
                      type: integer
                    - name: database_name
                      type: string
                    - name: sql
                      type: string
            examples:
              {'code':0, 'data': {'data_name' : 'pumu', 'database_id': 1, 'database_name': '...', 'sql': 'select ....'}}
        """
        data_link_id = str2int(data_link_id)
        result = DatabaseDataService.info(data_link_id=data_link_id)
        return jsonify(Response.correct(data=result))

    @error_handler
    def put(self, data_link_id: str):
        """
        修改数据库数据名称
        ---
        tags:
          - 数据库数据
        parameters:
          - name: data_link_id
            in: path
            type: integer
            required: true
            description: 数据链接id
          - name: data_name
            in: formData
            type: string
            required: true
          - name: ascription
            in: formData
            type: string
            default: project
            description: 该数据若归属于工程，传递project，若归属于应用，传递application，不传值默认为project
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
              {'message': {'ValueError': 'Error data link id'}, 'code': 1}
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
        args = DatabaseDataOperatorPut.parse_args()
        data_name: str = args['data_name']
        ascription = args['ascription'] or 'project'
        data_link_id = str2int(data_link_id)
        if 'project' == ascription:
            ProDatabaseDataService.rename(data_link_id=data_link_id, data_name=data_name)
        elif 'application' == ascription:
            AppDatabaseDataService.rename(data_link_id=data_link_id, data_name=data_name)
        return jsonify(Response.correct())

    @error_handler
    def delete(self, data_link_id: str):
        """
        删除数据库数据
        ---
        tags:
          - 数据库数据
        parameters:
          - name: data_link_id
            in: path
            type: integer
            required: true
          - name: is_forced
            in: formData
            type: integer
            default: 0
            description: 是否在被模型使用的情况下强制删除,0(默认)表示否,1表示强制删除（只适用于工程下数据）
          - name: ascription
            in: formData
            type: string
            default: project
            description: 该数据若归属于工程，传递project，若归属于应用，传递application，不传值默认为project
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
              {'message': {'ValueError': 'Error data link id'}, 'code': 1}
          200:
            description: 删除状态，若code为0，删除成功，若为2，则需要强制删除
            schema:
              properties:
                code:
                  type: integer
            examples:
              {'code': 0}
        """
        args = DatabaseDataOperatorDelete.parse_args()
        is_forced = args['is_forced'] or 0
        data_link_id = str2int(data_link_id)
        ascription = args['ascription'] or 'project'
        if 'project' == ascription:
            status: bool = ProDatabaseDataService.delete(data_link_id=data_link_id, is_forced=is_forced)
        else:
            status: bool = AppDatabaseDataService.delete(data_link_id=data_link_id)
        if status:
            return jsonify(Response.correct())
        else:
            return jsonify(Response.force())


DatabaseDataDataGet = reqparse.RequestParser()
# DatabaseDataDataGet.add_argument('data_type', required=True, type=str, location='args', choices=PermitDatabaseType)
DatabaseDataDataGet.add_argument('page', required=True, type=int, location='args')
DatabaseDataDataGet.add_argument('limit', required=True, type=int, location='args')


class DatabaseDataData(Resource):

    @error_handler
    def get(self, data_link_id: str):
        """
        获取数据库数据的数据
        ---
        tags:
          - 数据库数据
        parameters:
          - name: data_link_id
            in: path
            type: integer
            required: true
            description: 数据链接id
          - name: page
            in: query
            type: integer
            required: true
            description: 页码
          - name: limit
            in: query
            type: integer
            required: true
            description: 每页数据量
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
              {'message': {'ValueError': 'Error data link id'}, 'code': 1}
          200:
            schema:
              properties:
                data:
                  type: array
                  description: 数据链接数据
                  items:
                   - name: a
                     type: integer
                   - name: b
                     type: integer
                record:
                  type: integer
                  description: 数据量
                code:
                  type: integer
                  default: 0
                page:
                  type: integer
                limit:
                  type: integer
                total_page:
                  type: integer
            examples:
              {'data' : [{'a':1, 'b':2}, {'a': 2, 'b': 3}], 'record': 2, 'code': 0, 'page': 1, 'limit': 20, 'total_page': 20}
        """
        args = DatabaseDataDataGet.parse_args()
        page = args['page']
        limit = args['limit']
        data_link_id = str2int(data_link_id)
        data, record = DatabaseDataService.get(data_link_id=data_link_id, page=page - 1, limit=limit)
        total_page = math.ceil(record / limit)
        if page <= total_page:
            return jsonify(Response.correct(data=data.to_dict(orient='record'), record=record, page=page, limit=limit,
                                            total_page=total_page))
        else:
            raise RequestValueError('Page number {} exceeds the total number of pages {}'.format(page, total_page))


class DatabaseDataOverview(Resource):

    @error_handler
    def get(self, data_link_id: str):
        """
        获取数据库数据概览
        ---
        tags:
          - 数据库数据
        parameters:
          - name: data_link_id
            in: path
            type: integer
            required: true
            description: 数据链接id
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
              {'message': {'ValueError': 'Error data link id'}, 'code': 1}
          200:
            schema:
              properties:
                data:
                  type: array
                  description: 数据链接数据概览
                  items:
                    - name: record
                      type: integer
                      description: 数据量
                    - name: overview
                      type: array
                      items:
                        - name: column
                          type: string
                        - name: type
                          type: string
                        - name: range
                          type: array
                          items:
                            type: string
                        - name: na_count
                          type: integer
                        - name: outliers_count
                          type: string
                        - name: count
                          type: integer
                        - name: mean
                          type: float
                        - name: std
                          type: float
                        - name: 25%
                          type: float
                        - name: 50%
                          type: float
                        - name: 75%
                          type: float
                        - name: min
                          type: float
                        - name: max
                          type: float
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'data' : [{'record': 14, 'overview': [{'column': '员工', 'type': 'float64', 'range': ['0', '100'], 'na_count': 12, 'outliers_count': 2, 'count': 100, 'mean': 50, 'std': 210, '50%': 51, '75%': 79, '25%': 30, 'max': 100, 'min': 0}]}]}
        """
        data_link_id = str2int(data_link_id)
        data = DatabaseDataService.overview(data_link_id=data_link_id)
        return jsonify(Response.correct(data=data))
