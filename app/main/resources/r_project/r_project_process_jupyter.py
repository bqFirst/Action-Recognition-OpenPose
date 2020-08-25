#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/29 9:59
# @Author : wangweimin
# @File   : r_project_process_jupyter.py
# @Desc   :

import os
import pandas as pd

from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.resources_response import Response
from app.main.resources.r_base.request_data_transform import str2pd
from app.main.services.core.data.project_file_operator import ProjectDataOperator
from app.main.services.operator.project_operator.project_process_data_operator import ProjectProcessService
from app.models import DataSourceDataLink
from conf.data_path import DataDirectoryPath

ProjectDataByNameGet = reqparse.RequestParser()
ProjectDataByNameGet.add_argument('project_path', type=str, required=True, location='args')
ProjectDataByNameGet.add_argument('data_type', type=str, required=True, location='args', choices=('src', 'process'))
ProjectDataByNameGet.add_argument('data_name', type=str, required=True, location='args')
ProjectDataByNameGet.add_argument('sql', type=str, location='form')


ProjectDataByNamePost = reqparse.RequestParser()
ProjectDataByNamePost.add_argument('project_path', type=str, required=True, location='args')
ProjectDataByNamePost.add_argument('data_name', type=str, required=True, location='args')
ProjectDataByNamePost.add_argument('data', type=str2pd, required=True, location='form')


class ProjectDataByName(Resource):

    @error_handler
    def get(self):
        """
        通过文件名获取工程关联数据链接数据，jupyter使用
        ---
        tags:
          - 工程过程数据
        parameters:
          - name: project_path
            in: query
            type: string
            required: true
          - name: data_type
            in: query
            type: string
            required: true
          - name: data_name
            in: query
            type: string
            required: true
          - name: sql
            in: formData
            type: string
        responses:
          500:
            description: 获取失败
            schema:
              properties:
                message:
                  items:
                    - name: Error
                      type: string
            examples:
              {'message': {'ValueError': 'Error project path'}}
          200:
            description: 数据
            schema:
              properties:
                data:
                  type: array
                  items:
                    - name: column1
                      type: integer
                      description: 示例
            examples:
              {'data': [{'column1': 12}, {'column1': 13}]}
        """
        args = ProjectDataByNameGet.parse_args()
        project_path = args['project_path'].strip(os.path.sep)
        data_type = args['data_type']
        data_name = args['data_name']
        sql = args['sql']
        data_operator = ProjectDataOperator(project_path=project_path)
        if 'process' == data_type:
            data = data_operator.get_project_data(src=data_name)
        elif 'src' == data_type:
            data = data_operator.get_original_data(src=data_name, sql=sql)
            # data = data_operator.get_original_data(src=data_name)
        else:
            data = pd.DataFrame()
        return jsonify(Response.correct(data=data.to_dict(orient='records')))

    @error_handler
    def post(self):
        """
        存储工程中间数据，jupyter使用
        ---
        tags:
          - 工程过程数据
        parameters:
          - name: project_path
            in: query
            type: string
            required: true
          - name: data_name
            in: query
            type: string
            required: true
          - name: data
            in: formData
        responses:
          500:
            description: 存储失败
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
              {'message': {'ValueError': 'Error project path'}, 'code': 1}
          200:
            description: 数据
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                data_link_id:
                  type: integer
            examples:
              {'code': 0}
        """
        args = ProjectDataByNamePost.parse_args()
        project_path = args['project_path']
        data_name = args['data_name']
        data = args['data']
        # data_operator = ProjectDataOperator(project_path=project_path)
        # data_link_id = data_operator.create_data(data=data, filename=data_name)
        data_link_id = ProjectProcessService.create(data=data, filename=data_name, project_path=project_path)
        return jsonify(Response.correct(data_link_id=data_link_id))


ProjectDataRouteGet = reqparse.RequestParser()
ProjectDataRouteGet.add_argument('project_path', type=str, required=True, location='args')
ProjectDataRouteGet.add_argument('data_type', type=str, required=True, location='args', choices=('src', 'process'))
ProjectDataRouteGet.add_argument('data_name', type=str, required=True, location='args')


class ProjectDataRoute(Resource):

    @error_handler
    def get(self):
        """
        通过文件名获取工程关联数据链接数据绝对路径，jupyter使用
        ---
        tags:
          - 工程过程数据
        parameters:
          - name: project_path
            in: query
            type: string
            required: true
          - name: data_type
            in: query
            type: string
            required: true
          - name: data_name
            in: query
            type: string
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
            examples:
              {'message': {'ValueError': 'Error project path'}}
          200:
            description: 数据
            schema:
              properties:
                route:
                  type: string

            examples:
              {'route': '/path/to/file'}
        """
        args = ProjectDataRouteGet.parse_args()
        project_path = args['project_path']
        data_type = args['data_type']
        data_name = args['data_name']
        data_operator = ProjectDataOperator(project_path=project_path)
        if 'process' == data_type:
            data_alias = data_operator.get_project_data_alias(src=data_name)
            data_alias = os.path.join(DataDirectoryPath.get_project_path(), data_alias)
        else:
            data_link: DataSourceDataLink = data_operator.get_original_data_alias(src=data_name)
            data_type = data_link.data_type.data_type
            if 'distributed' == data_type:
                data_alias = os.path.join(DataDirectoryPath.get_distributed_path(), data_link.alias)
            else:
                raise TypeError('the data link is not distributed file data')
        return jsonify(Response.correct(route=data_alias))
