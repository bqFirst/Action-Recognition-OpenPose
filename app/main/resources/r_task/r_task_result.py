#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/2 9:37
# @Author : wangweimin
# @File   : r_task_result.py
# @Desc   :

import math

from flask import jsonify, send_from_directory
from flask_restful import Resource, reqparse

from app.main.basic_main.custom_error import RequestValueError
from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.task_operator.task_result_operator import TaskResultService


class TaskResultDataOperator(Resource):

    @error_handler
    def get(self, result_data_id):
        """
        导出离线任务结果数据
        ---
        tags:
          - 离线任务数据
        parameters:
          - name: result_data_id
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
              {'code': 1, 'message': {'ValueError': 'Error task id'}}
          200:
            description: 下载成功
        """
        result_data_id = str2int(result_data_id)
        directory, file, filename = TaskResultService.download(result_data_id=result_data_id)
        return send_from_directory(directory=directory, filename=file, as_attachment=True,
                                   attachment_filename=filename)


TaskResultDataDataGet = reqparse.RequestParser()
TaskResultDataDataGet.add_argument('page', type=int, required=True, location='args')
TaskResultDataDataGet.add_argument('limit', type=int, required=True, location='args')


class TaskResultDataData(Resource):

    @error_handler
    def get(self, result_data_id):
        """
        查看离线任务结果数据
        ---
        tags:
          - 离线任务数据
        parameters:
          - name: result_data_id
            in: path
            type: integer
            required: true
            description: 结果数据链接id
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
              {'code': 1, 'message': {'ValueError': 'Error data link id'}}
          200:
            description: 获取成功
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
        result_data_id = str2int(result_data_id)
        args = TaskResultDataDataGet.parse_args()
        page = args['page']
        limit = args['limit']
        data, record = TaskResultService.get(result_data_id=result_data_id, page=page-1, limit=limit)
        total_page = math.ceil(record / limit)
        if page <= total_page:
            return jsonify(
                Response.correct(data=data.to_dict(orient='record'), record=record, page=page, limit=limit,
                                 total_page=total_page))
        else:
            raise RequestValueError('Page number {} exceeds the total number of pages {}'.format(page, total_page))
