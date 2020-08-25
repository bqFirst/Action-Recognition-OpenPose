#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/19 14:44
# @Author : wangweimin
# @File   : r_project_process_data.py
# @Desc   :

import math

from flask import jsonify, send_from_directory
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.project_operator.project_process_data_operator import ProjectProcessService, \
    ProjectProcessesService


class PROJECTProcessData(Resource):

    @error_handler
    def get(self, project_id: str):
        """
        获取工程及其下过程数据链接信息
        ---
        tags:
          - 工程过程数据
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
                    - name: data_type
                      type: string
                    - name: create_time
                      type: string
                    - name: record
                      type: integer
                    - name: creator
                      type: string
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'project_id': 1, 'data': [{'data_link_id': 1, 'create_time': '2019-01-01 00:00:00', 'data_name': 'dn', 'data_type': 'csv', 'record': 300, 'creator': 'm'}, ]}
        """
        project_id = str2int(project_id)
        data = ProjectProcessesService.info(project_id=project_id)
        return jsonify(Response.correct(project_id=project_id, data=data))


PROJECTProcessDataDataGet = reqparse.RequestParser()
PROJECTProcessDataDataGet.add_argument('page', required=True, type=int, location='args')
PROJECTProcessDataDataGet.add_argument('limit', required=True, type=int, location='args')


class PROJECTProcessDataData(Resource):

    @error_handler
    def get(self, project_id: str, process_data_id: str):
        """
        获取工程过程数据的数据
        ---
        tags:
          - 工程过程数据
        parameters:
          - name: process_data_id
            in: path
            type: integer
            required: true
            description: 数据链接id
          - name: project_id
            in: path
            type: string
            required: true
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
              {'data' : [{'a':1, 'b':2}, {'a': 2, 'b': 3}], 'record': 2, 'code': 0, 'page': 1, 'limit': 20, 'total_page': 2}
        """
        args = PROJECTProcessDataDataGet.parse_args()
        page = args['page']
        limit = args['limit']
        process_data_id = str2int(process_data_id)
        project_id = str2int(project_id)
        data, record = ProjectProcessService.get(project_id=project_id, process_data_id=process_data_id,
                                                 page=page - 1,
                                                 limit=limit)
        total_page = math.ceil(record / limit)
        if page <= total_page:
            return jsonify(
                Response.correct(data=data.to_dict(orient='record'), record=record, page=page, limit=limit,
                                 total_page=total_page))
        else:
            raise ValueError('Page number {} exceeds the total number of pages {}'.format(page, total_page))


PROJECTProcessDataOperatorPut = reqparse.RequestParser()
PROJECTProcessDataOperatorPut.add_argument('data_name', type=str, required=True, location='form')


class PROJECTProcessDataOperator(Resource):

    @error_handler
    def get(self, project_id: str, process_data_id: str):
        """
        下载工程过程数据
        ---
        tags:
          - 工程过程数据
        parameters:
          - name: process_data_id
            in: path
            type: string
            required: true
          - name: project_id
            in: path
            type: string
            required: true
        responses:
          500:
            description: 下载失败
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
              {'message': {'ValueError': 'Error project process data id'}, 'code': 1}
          200:
            description: 下载成功，返回数据
        """
        project_id = str2int(project_id)
        process_data_id = str2int(process_data_id)
        directory, file, filename = ProjectProcessService.download(project_id=project_id,
                                                                   process_data_id=process_data_id)
        return send_from_directory(directory=directory, filename=file, as_attachment=True,
                                   attachment_filename=filename)

    @error_handler
    def delete(self, project_id: str, process_data_id: str):
        """
        删除工程过程数据
        ---
        tags:
          - 工程过程数据
        parameters:
          - name: process_data_id
            in: path
            type: string
            required: true
          - name: project_id
            in: path
            type: string
            required: true
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
                  default: 0
            examples:
              {'message': {'ValueError': 'Error project process data id'}, 'code': 1}
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
        process_data_id = str2int(process_data_id)
        project_id = str2int(project_id)
        ProjectProcessService.delete(project_id=project_id, process_data_id=process_data_id)
        return jsonify(Response.correct())

    @error_handler
    def put(self, project_id: str, process_data_id: str):
        """
        修改工程过程数据名称
        ---
        tags:
          - 工程过程数据
        parameters:
          - name: process_data_id
            in: path
            type: string
            required: true
          - name: project_id
            in: path
            type: string
            required: true
          - name: data_name
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
                  default: 0
            examples:
              {'message': {'ValueError': 'Error project process data id'}, 'code': 1}
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

        args = PROJECTProcessDataOperatorPut.parse_args()
        data_name = args['data_name']
        process_data_id = str2int(process_data_id)
        project_id = str2int(project_id)
        ProjectProcessService.rename(project_id=project_id, process_data_id=process_data_id,
                                     data_name=data_name)
        return jsonify(Response.correct())
