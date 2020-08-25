#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/2 15:51
# @Author : wangweimin
# @File   : r_data_source_data.py
# @Desc   :

import math
import os
import pandas as pd
# import traceback

from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.basic_main.custom_error import RequestValueError
from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.resources.resources_config import PermitFileType, PermitAscriptionType
from app.main.services.operator.data_source_data_operator.application_data_source_csv_operator import AppDsCsvService
from app.main.services.operator.data_source_data_operator.project_data_source_csv_operator import ProDsCsvService
from app.main.services.operator.data_source_data_operator.application_data_source_excel_operator import \
    AppDsExcelService
from app.main.services.operator.data_source_data_operator.project_data_source_excel_operator import ProDsExcelService
from app.main.services.operator.data_source_data_operator.data_source_iexcel_operator import DsExcelService
from app.main.services.operator.data_source_data_operator.data_source_icsv_operator import DsCsvService
from app.main.services.operator.data_source_data_operator.data_source_data_operator import \
    ds_data_link_sheet_delete_service
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.models import DataSourceDataLink
from conf.data_path import DataDirectoryPath

DSDataLinkOperatorGet = reqparse.RequestParser()
DSDataLinkOperatorGet.add_argument('data_type', required=True, type=str, location='form', choices=PermitFileType)

DSDataLinkOperatorPut = reqparse.RequestParser()
DSDataLinkOperatorPut.add_argument('data_link_name', required=True, type=str, location='form')
DSDataLinkOperatorPut.add_argument('catalog_id', type=int, location='form')
DSDataLinkOperatorPut.add_argument('data_type', required=True, type=str, location='form', choices=PermitFileType)
DSDataLinkOperatorPut.add_argument('ascription', type=str, location='form', choices=PermitAscriptionType)

DSDataLinkOperatorDelete = reqparse.RequestParser()
DSDataLinkOperatorDelete.add_argument('is_forced', type=int, location='form', choices=(0, 1))
DSDataLinkOperatorDelete.add_argument('data_type', required=True, type=str, location='form', choices=PermitFileType)
DSDataLinkOperatorDelete.add_argument('ascription', type=str, location='form', choices=PermitAscriptionType)


class DSDataLinkOperator(Resource):

    @staticmethod
    def get_sheet(data_link: DataSourceDataLink) -> list:
        alias: str = data_link.alias
        if alias.endswith(('xls', 'xlsx', 'excel')):
            file = os.path.join(DataDirectoryPath.get_data_source_path(), alias)
            reader = pd.ExcelFile(file)
            sheet_names: list = reader.sheet_names
            return [{'sheet_name': sheet_name} for sheet_name in sheet_names]
        elif alias.endswith('csv'):
            return [{'sheet_name': data_link.name}]
        else:
            return []

    def unused_get(self, data_link_id: str):
        """
        获取数据链接信息（暂时无用）
        ---
        tags:
          - 数据源数据链接
        parameters:
          - name: data_link_id
            in: path
            type: integer
            required: true
            description: 数据链接id
          - name: data_type
            in: formData
            required: true
            description: 数据链接的类型，'csv'或者'excel'等
            schema:
              type: string
              enum:
                - csv
                - excel
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
                data:
                  type: array
                  description: 数据链接数据
                  items:
                   - name: sheet_name
                     type: string
                code:
                  type: integer
                  default: 0
            examples:
              {'code':0, 'data' : [{'sheet_name': 'sheet1'}, {'sheet_name': 'sheet2'}]}
        """

        try:
            data_link_id = str2int(data_link_id)
            data_link: DataSourceDataLink = DataSourceDataLink.query.get(data_link_id)
            if not data_link:
                raise ValueError('Error data link id')
            else:
                res = Response.correct()
                res.update(data=self.get_sheet(data_link=data_link))
        except Exception as e:
            res = Response.error()
            res.update(message={'Error': str(e)})
        return jsonify(res)

    @error_handler
    def put(self, data_link_id: str):
        """
        修改数据链接名称或所属数据源目录
        ---
        tags:
          - 数据源数据链接
        parameters:
          - name: data_link_id
            in: path
            type: integer
            required: true
            description: 数据链接id
          - name: data_link_name
            in: formData
            type: string
            required: true
          - name: catalog_id
            in: formData
            type: integer
            description: 数据源目录id，0.3版本后取消（不传参）
          - name: ascription
            in: formData
            type: string
            default: project
            description: 该数据若归属于工程，传递project，若归属于应用，传递application，不传值默认为project
          - name: data_type
            in: formData
            required: true
            description: 数据链接的类型，'csv'或者'excel'等
            schema:
              type: string
              enum:
                - csv
                - excel
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
        args = DSDataLinkOperatorPut.parse_args()
        new_name = args['data_link_name']
        catalog_id: int = None
        # catalog_id = args['catalog_id']
        data_type = args['data_type']
        data_link_id = str2int(data_link_id)
        ascription = args['ascription'] or 'project'
        if 'project' == ascription:
            if 'excel' == data_type:
                ProDsExcelService.rename(data_link_id=data_link_id, new_name=new_name, catalog_id=catalog_id)
            elif 'csv' == data_type:
                ProDsCsvService.rename(data_link_id=data_link_id, new_name=new_name, catalog_id=catalog_id)
            else:
                pass
        elif 'application' == ascription:
            if 'excel' == data_type:
                AppDsExcelService.rename(data_link_id=data_link_id, new_name=new_name, catalog_id=catalog_id)
            elif 'csv' == data_type:
                AppDsCsvService.rename(data_link_id=data_link_id, new_name=new_name, catalog_id=catalog_id)
            else:
                pass
        return jsonify(Response.correct())

    @error_handler
    def delete(self, data_link_id: str):
        """
        删除数据链接
        ---
        tags:
          - 数据源数据链接
        parameters:
          - name: data_link_id
            in: path
            type: integer
            required: true
          - name: is_forced
            in: formData
            type: integer
            default: 0
            description: 是否在被模型使用的情况下强制删除,0(默认)表示否,1表示强制删除（只适用于工程数据）
          - name: ascription
            in: formData
            type: string
            default: project
            description: 该数据若归属于工程，传递project，若归属于应用，传递application，不传值默认为project
          - name: data_type
            in: formData
            required: true
            description: 数据链接的类型，'csv'或者'excel'等
            schema:
              type: string
              enum:
                - csv
                - excel
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
                  default: 0
            examples:
              {'code': 0}
        """
        args = DSDataLinkOperatorDelete.parse_args()
        is_forced = args['is_forced'] or 0
        data_type = args['data_type']
        data_link_id = str2int(data_link_id)
        ascription = args['ascription'] or 'project'
        if 'project' == ascription:
            if 'excel' == data_type:
                status = ProDsExcelService.delete(data_link_id=data_link_id, is_forced=is_forced)
            elif 'csv' == data_type:
                status = ProDsCsvService.delete(data_link_id=data_link_id, is_forced=is_forced)
            else:
                raise TypeError
        elif 'application' == ascription:
            if 'excel' == data_type:
                status = AppDsExcelService.delete(data_link_id=data_link_id)
            elif 'csv' == data_type:
                status = AppDsCsvService.delete(data_link_id=data_link_id)
            else:
                raise TypeError
        else:
            raise TypeError
        if status:
            return jsonify(Response.correct())
        else:
            return jsonify(Response.force())


# get与delete共用
DSDataLinkDataQuery = reqparse.RequestParser()
DSDataLinkDataQuery.add_argument('data_type', required=True, type=str, location='args', choices=PermitFileType)
DSDataLinkDataQuery.add_argument('page', required=True, type=int, location='args')
DSDataLinkDataQuery.add_argument('limit', required=True, type=int, location='args')


# DSDataLinkDataQuery.add_argument('sheet_name', type=str, location='args', required=True)


class DSDataLinkData(Resource):

    @staticmethod
    def get_sheet_data(data_link: DataSourceDataLink, sheet_name: str) -> list:
        alias: str = data_link.alias
        if alias.endswith(('xlsx', 'xls', 'excel')):
            reader = pd.ExcelFile(os.path.join(DataDirectoryPath.get_data_source_path(), alias))
            data: pd.DataFrame = reader.parse(sheet_name)
        elif alias.endswith('csv'):
            data: pd.DataFrame = DataFileOperator(address='data_source').get(filename=alias)
        else:
            data: pd.DataFrame = pd.DataFrame()
        data: pd.DataFrame = data.fillna('')
        return data.to_dict(orient='record')

    @error_handler
    def get(self, data_link_id: str):
        """
        获取数据链接数据
        ---
        tags:
          - 数据源数据链接
        parameters:
          - name: data_link_id
            in: path
            type: integer
            required: true
            description: 数据链接id
          - name: data_type
            in: query
            required: true
            description: 数据链接的类型，'csv'或者'excel'等
            schema:
              type: string
              enum:
                - csv
                - excel
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
        args = DSDataLinkDataQuery.parse_args()
        data_type = args['data_type']
        page = args['page']
        limit = args['limit']
        data_link_id = str2int(data_link_id)
        if 'excel' == data_type:
            data, record = DsExcelService.get(data_link_id=data_link_id, page=page - 1, limit=limit)
        elif 'csv' == data_type:
            data, record = DsCsvService.get(data_link_id=data_link_id, page=page - 1, limit=limit)
        else:
            raise TypeError
        total_page = math.ceil(record / limit)
        if page <= total_page:
            return jsonify(
                Response.correct(data=data.to_dict(orient='record'), record=record, page=page, limit=limit,
                                 total_page=total_page))
        else:
            raise RequestValueError('Page number {} exceeds the total number of pages {}'.format(page, total_page))

    @error_handler
    def unused_delete(self, data_link_id: str):
        """
        删除数据链接或其分页（0.3版本开始不使用）
        ---
        tags:
          - 数据源数据链接
        parameters:
          - name: data_link_id
            in: path
            type: integer
            required: true
          - name: sheet_name
            in: query
            type: string
            description: 需要删除的分页名称，若只剩一个分页，删除文件
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
            description: 删除成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0}
        """
        args = DSDataLinkDataQuery.parse_args()
        sheet_name: str = args['sheet_name']
        try:
            data_link_id = str2int(data_link_id)
            ds_data_link_sheet_delete_service(data_sheet_id=data_link_id)
            return jsonify(Response.correct())
        except Exception as e:
            return jsonify(Response.error(message={'Error': str(e)}))


DSDataLinkOverviewGet = reqparse.RequestParser()
DSDataLinkOverviewGet.add_argument('data_type', required=True, type=str, location='args', choices=PermitFileType)


class DSDataLinkOverview(Resource):

    @error_handler
    def get(self, data_link_id: str):
        """
        获取数据链接数据概览
        ---
        tags:
          - 数据源数据链接
        parameters:
          - name: data_link_id
            in: path
            type: integer
            required: true
            description: 数据链接id
          - name: data_type
            in: query
            required: true
            description: 数据链接的类型，'csv'或者'excel'等
            schema:
              type: string
              enum:
                - csv
                - excel
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
        args = DSDataLinkOverviewGet.parse_args()
        data_type = args['data_type']
        data_link_id = str2int(data_link_id)
        if 'excel' == data_type:
            data = DsExcelService.overview(data_link_id=data_link_id)
        elif 'csv' == data_type:
            data = DsCsvService.overview(data_link_id=data_link_id)
        else:
            raise TypeError
        return jsonify(Response.correct(data=data))
