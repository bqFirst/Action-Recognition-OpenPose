#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/29 16:26
# @Author : wangweimin
# @File   : r_application_src_data.py
# @Desc   :

from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.resources.resources_config import PermitApplicationSrcType
from app.main.services.operator.application_operator.application_src_data_operator import ApplicationSrcDataService
from app.main.services.operator.data_source_data_operator.application_data_source_excel_operator import \
    AppDsExcelService
from app.main.services.operator.data_source_data_operator.application_data_source_csv_operator import AppDsCsvService
from app.main.services.operator.database_operator.application_database_data_operator import AppDatabaseDataService
from app.main.services.operator.picture_operator.application_picture_catalog_operator import AppPictureCatalogService

ApplicationSrcDataPut = reqparse.RequestParser()
ApplicationSrcDataPut.add_argument('data_name', required=True, type=str, location='form')


class ApplicationSrcData(Resource):

    @error_handler
    def get(self, application_id: str):
        """
        获取应用及其下数据链接信息
        ---
        tags:
          - 应用数据
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
              {'message': {'ValueError': 'Error application id'}, 'code': 1}
          200:
            schema:
              properties:
                application_id:
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
                    - name: creator
                      type: string
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'application_id': 1, 'data': [{'creator': 'm', 'data_link_id': 1, 'data_name': 'dn', 'create_time': '2019-01-01 00:00:00', 'data_type': 'csv', 'record': 300}, ]}
        """
        application_id = str2int(application_id)
        data = ApplicationSrcDataService.info(application_id=application_id)
        return jsonify(Response.correct(application_id=application_id, data=data))

    @error_handler
    def put(self, application_id: str):
        """
        验证应用数据名称是否重复
        ---
        tags:
          - 应用数据
        parameters:
          - name: application_id
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
              {'message': {'ValueError': 'Error application id'}, 'code': 1}
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
        args = ApplicationSrcDataPut.parse_args()
        data_name = args['data_name']
        application_id = str2int(application_id)
        status = ApplicationSrcDataService.name_verify(application_id=application_id, data_name=data_name)
        if status:
            return jsonify(Response.correct())
        else:
            return jsonify(Response.name_repeated())


ApplicationSrcDataOperatorPut = reqparse.RequestParser()
ApplicationSrcDataOperatorPut.add_argument('data_name', type=str, required=True, location='form')
ApplicationSrcDataOperatorPut.add_argument('data_type', type=str, required=True, location='form',
                                           choices=PermitApplicationSrcType)


class ApplicationSrcDataOperator(Resource):

    @error_handler
    def put(self, application_id: str, data_link_id: str):
        """
        修改应用数据名称
        ---
        tags:
          - 应用数据
        parameters:
          - name: application_id
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
        args = ApplicationSrcDataOperatorPut.parse_args()
        data_name = args['data_name']
        data_type = args['data_type']
        catalog_id: int = None

        application_id = str2int(application_id)
        data_link_id = str2int(data_link_id)
        if 'excel' == data_type:
            AppDsExcelService.rename(data_link_id=data_link_id, new_name=data_name, catalog_id=catalog_id,
                                     application_id=application_id)
        elif 'csv' == data_type:
            AppDsCsvService.rename(data_link_id=data_link_id, new_name=data_name, catalog_id=catalog_id,
                                   application_id=application_id)
        elif 'picture' == data_type:
            AppPictureCatalogService.rename(catalog_id=data_link_id, catalog_name=data_name,
                                            application_id=application_id)
        elif 'MySQL' == data_type:
            AppDatabaseDataService.rename(data_link_id=data_link_id, data_name=data_name, application_id=application_id)
        else:
            return jsonify(Response.error(message={'Error': '不存在数据类型{}'.format(data_type)}))
        return jsonify(Response.correct())
