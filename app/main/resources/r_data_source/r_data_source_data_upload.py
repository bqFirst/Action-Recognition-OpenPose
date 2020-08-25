#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/11 11:26
# @Author : wangweimin
# @File   : r_data_source_data_upload.py
# @Desc   :

import time

from werkzeug.datastructures import FileStorage

from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_param_judgement import one_and_the_only
from app.main.resources.r_base.request_data_transform import str2dict
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.data_source_data_operator.application_data_source_csv_operator import AppDsCsvService
from app.main.services.operator.data_source_data_operator.project_data_source_csv_operator import ProDsCsvService
from app.main.services.operator.data_source_data_operator.application_data_source_excel_operator import \
    AppDsExcelService
from app.main.services.operator.data_source_data_operator.data_source_iexcel_operator import DsExcelService
from app.main.services.operator.data_source_data_operator.project_data_source_excel_operator import ProDsExcelService
from app.models import User

DSDataCsvPost = reqparse.RequestParser()
DSDataCsvPost.add_argument('catalog_id', type=int, location='form')
DSDataCsvPost.add_argument('data_type', required=True, type=str, location='form', choices=('csv',))
DSDataCsvPost.add_argument('data_name', required=True, type=str, location='form')
DSDataCsvPost.add_argument('project_id', type=str, location='form')
DSDataCsvPost.add_argument('application_id', type=str, location='form')
DSDataCsvPost.add_argument('file', required=True, type=FileStorage, location='files')


class DSDataCsv(Resource):

    @error_handler
    def post(self):
        """
        新建数据链接——上传数据文件(csv格式)
        ---
        tags:
          - 数据源数据链接
        parameters:
          - name: project_id
            in: formData
            type: integer
            description: 若为应用数据，不传递该参数
          - name: application_id
            in: formData
            type: integer
            description: 若为工程原始数据，不传递该参数
          - name: data_type
            in: formData
            required: true
            description: 数据链接的类型，'csv'
          - name: data_name
            in: formData
            type: string
            required: true
            description: 数据链接名称
          - name: file
            in: formData
            required: true
            type: file
            description: 文件流
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
              {'message': {'ValueError': 'Error catalog id'}, 'code': 1}
          200:
            description: 新建数据链接成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                data_link_id:
                  type: integer
            examples:
              {'code': 0, 'data_link_id': 1}
        """
        args = DSDataCsvPost.parse_args()
        data_type = args['data_type']
        data_name = args['data_name']
        catalog_id = args['catalog_id'] or 1  # 0.1版本中带有数据源目录
        f = args['file']
        project_id = args['project_id'] or None
        application_id = args['application_id'] or None
        one_and_the_only(project_id, application_id)
        user_id = User.query.first().id
        if project_id:
            data_link_id = ProDsCsvService.upload(f=f, catalog_id=catalog_id, user_id=user_id, data_name=data_name,
                                                  data_type=data_type, project_id=project_id)
        else:
            data_link_id = AppDsCsvService.upload(f=f, catalog_id=catalog_id, user_id=user_id, data_name=data_name,
                                                  data_type=data_type, application_id=application_id)
        return jsonify(Response.correct(data_link_id=data_link_id))


DSDataExcelPost = reqparse.RequestParser()
DSDataExcelPost.add_argument('file', required=True, type=FileStorage, location='files')
DSDataExcelPost.add_argument('data_type', required=True, type=str, location='form', choices=('excel',))

DSDataExcelDelete = reqparse.RequestParser()
DSDataExcelDelete.add_argument('uuid', required=True, type=str, location='form')
DSDataExcelDelete.add_argument('data_type', required=True, type=str, location='form', choices=('excel',))

DSDataExcelPut = reqparse.RequestParser()
DSDataExcelPut.add_argument('catalog_id', type=int, location='form')
DSDataExcelPut.add_argument('data_type', required=True, type=str, location='form', choices=('excel',))
DSDataExcelPut.add_argument('data_name_map', required=True, type=str2dict, location='form')
DSDataExcelPut.add_argument('project_id', type=str, location='form')
DSDataExcelPut.add_argument('application_id', type=str, location='form')
DSDataExcelPut.add_argument('uuid', required=True, type=str, location='form')


class DSDataExcel(Resource):
    """
    本resource的post和put方法意义互换了
    """

    @error_handler
    def post(self):
        """
        仅上传数据文件(excel格式)，并进行解析sheet页
        ---
        tags:
          - 数据源数据链接
        parameters:
          - name: data_type
            in: formData
            required: true
            description: 数据链接的类型，'excel'
          - name: file
            in: formData
            required: true
            type: file
            description: 文件流
        responses:
          500:
            description: 上传失败
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
            description: 上传数据链接成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                uuid:
                  type: string
                sheet_names:
                  type: array
                  items:
                    type: string
            examples:
              {'code': 0, 'uuid': 'fc833fb89d264167ad6f549ebabfc0dd', 'sheet_name': ['sheet1', 'sheet2']}
        """
        args = DSDataExcelPost.parse_args()
        time1 = time.time()
        f = args['file']
        print(time.time() - time1)
        result = DsExcelService.upload_post(f=f)
        print(time.time() - time1)
        return jsonify(Response.correct(**result))

    @error_handler
    def delete(self):
        """
        取消上传的数据文件(excel格式)
        ---
        tags:
          - 数据源数据链接
        parameters:
          - name: data_type
            in: formData
            required: true
            description: 数据链接的类型，'excel'
          - name: uuid
            in: formData
            required: True
            type: string
            description: 文件唯一标识符
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
              {'message': {'ValueError': 'Error message'}, 'code': 1}
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
        args = DSDataExcelDelete.parse_args()
        uuid_ = args['uuid']
        DsExcelService.upload_delete(uuid_=uuid_)
        return jsonify(Response.correct())

    @error_handler
    def put(self):
        """
        新建数据链接(excel格式)
        ---
        tags:
          - 数据源数据链接
        parameters:
          - name: project_id
            in: formData
            type: integer
            description: 若为应用数据，不传递该参数
          - name: application_id
            in: formData
            type: integer
            description: 若为工程原始数据，不传递该参数
          - name: data_type
            in: formData
            required: true
            description: 数据链接的类型，'excel'
          - name: data_name_map
            in: formData
            type: string
            required: true
            description: 数据链接sheet名称，key为旧名称，value为新名称，json数据
          - name: uuid
            in: formData
            required: True
            type: string
            description: 文件唯一标识符
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
              {'message': {'ValueError': 'Error catalog id'}, 'code': 1}
          200:
            description: 新建数据链接成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                data_link_id:
                  type: array
                  items:
                    type: integer
            examples:
              {'code': 0}
        """
        args = DSDataExcelPut.parse_args()
        data_type = args['data_type']
        data_name_map: dict = args['data_name_map']
        catalog_id = 1  # 0.1版本中带有数据源目录
        uuid_ = args['uuid']
        project_id = args['project_id'] or None
        application_id = args['application_id'] or None
        one_and_the_only(project_id, application_id)
        user_id = User.query.first().id
        if project_id:
            data_link_id = ProDsExcelService.upload_put(catalog_id=catalog_id, data_type=data_type,
                                                        data_name_map=data_name_map,
                                                        project_id=project_id, uuid_=uuid_, user_id=user_id)
        else:
            data_link_id = AppDsExcelService.upload_put(catalog_id=catalog_id, data_type=data_type,
                                                        data_name_map=data_name_map,
                                                        application_id=application_id, uuid_=uuid_, user_id=user_id)
        return jsonify(Response.correct(data_link_id=data_link_id))
