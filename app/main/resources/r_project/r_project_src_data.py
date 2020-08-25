#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/24 9:44
# @Author : wangweimin
# @File   : r_project_src_data.py
# @Desc   :

from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.resources_config import PermitProjectSrcType
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.data_source_data_operator.project_data_source_excel_operator import ProDsExcelService
from app.main.services.operator.data_source_data_operator.project_data_source_csv_operator import ProDsCsvService
from app.main.services.operator.database_operator.project_database_data_operator import ProDatabaseDataService
from app.main.services.operator.picture_operator.project_picture_catalog_operator import ProPictureCatalogService
from app.main.services.operator.project_operator.project_src_data_operator import ProjectSrcDataService

ProjectSrcDataPut = reqparse.RequestParser()
ProjectSrcDataPut.add_argument('data_name', required=True, type=str, location='form')


class ProjectSrcData(Resource):

    @error_handler
    def get(self, project_id: str):
        """
        获取工程及其下原始数据链接信息
        ---
        tags:
          - 工程原始数据
        parameters:
          - name: project_id
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
              {'message': {'ValueError': 'Error project id'}, 'code': 1}
          200:
            schema:
              properties:
                project_id:
                  type: integer
                data:
                  type: array
                  items:
                    - name: data_link_id
                      type: integer
                    - name: data_name
                      type: string
                    - name: create_time
                      type: string
                    - name: data_type
                      type: string
                    - name: record
                      type: integer
                      description: 记录数
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'project_id': 1, 'data': [{'data_link_id': 1, 'data_name': 'dn', 'create_time': '2019-01-01 00:00:00', 'data_type': 'csv', 'record': 300}, ]}
        """
        project_id = str2int(project_id)
        data = ProjectSrcDataService.info(project_id=project_id)
        return jsonify(Response.correct(project_id=project_id, data=data))

    @error_handler
    def put(self, project_id: str):
        """
        验证工程原始数据名称是否重复
        ---
        tags:
          - 工程原始数据
        parameters:
          - name: project_id
            in: path
            type: integer
            required: true
          - name: data_name
            in: formData
            type: string
            required: true
            description: 需要验证的数据名称
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
              {'message': {'ValueError': 'Error project id'}, 'code': 1}
          200:
            description: 验证成功，0表示无重复，3表示名称重复
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                  description: 0表示无重复，3表示名称重复
            examples:
              {'code': 0}
        """
        args = ProjectSrcDataPut.parse_args()
        data_name = args['data_name']
        project_id = str2int(project_id)
        status = ProjectSrcDataService.name_verify(project_id=project_id, data_name=data_name)
        if status:
            return jsonify(Response.correct())
        else:
            return jsonify(Response.name_repeated())


ProjectSrcDataOperatorPut = reqparse.RequestParser()
ProjectSrcDataOperatorPut.add_argument('data_name', type=str, required=True, location='form')
ProjectSrcDataOperatorPut.add_argument('data_type', type=str, required=True, location='form',
                                       choices=PermitProjectSrcType)


class ProjectSrcDataOperator(Resource):

    @error_handler
    def put(self, project_id: str, data_link_id: str):
        """
        修改工程原始数据名称
        ---
        tags:
          - 工程原始数据
        parameters:
          - name: project_id
            in: path
            type: integer
            required: true
          - name: data_link_id
            in: path
            type: integer
            required: true
          - name: data_name
            in: formData
            type: string
            required: true
          - name: data_type
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
        args = ProjectSrcDataOperatorPut.parse_args()
        data_name = args['data_name']
        data_type = args['data_type']
        catalog_id: int = None
        project_id = str2int(project_id)
        data_link_id = str2int(data_link_id)
        if 'excel' == data_type:
            ProDsExcelService.rename(data_link_id=data_link_id, new_name=data_name, catalog_id=catalog_id,
                                     project_id=project_id)
        elif 'csv' == data_type:
            ProDsCsvService.rename(data_link_id=data_link_id, new_name=data_name, catalog_id=catalog_id,
                                   project_id=project_id)
        elif 'picture' == data_type:
            ProPictureCatalogService.rename(catalog_id=data_link_id, catalog_name=data_name, project_id=project_id)
        elif 'MySQL' == data_type:
            ProDatabaseDataService.rename(data_link_id=data_link_id, data_name=data_name, project_id=project_id)
        else:
            return jsonify(Response.error(message={'Error': '不存在数据类型{}'.format(data_type)}))
        return jsonify(Response.correct())
