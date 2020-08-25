#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/2/10 16:09
# @Author : wangweimin
# @File   : r_case_task.py
# @Desc   :

from flask import jsonify, request
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.case_operator.case_task_operator import CaseTaskService

CASETaskPost = reqparse.RequestParser()
CASETaskPost.add_argument('mode_id', required=True, type=int, location='form')


class CASETask(Resource):

    @error_handler
    def post(self, case_id):
        """
        创建案例任务，实际所需数据参数根据不同的案例不同！以下为必要的两个参数，其余参数未列出（该接口无法通过该接口文档使用）
        ---
        tags:
          - 案例任务
        parameters:
          - name: case_id
            in: path
            type: string
            required: true
          - name: mode_id
            in: formData
            type: integer
            required: true
            description: 模式id
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
              {'code': 1, 'message': {'ValueError': 'Error case id'}}
          200:
            description: 创建成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                data:
                  description: 根据案例不同，返回的参数不同
                  items:
                    - name: picture_name
                      type: string
            examples:
              {'code': 0, 'data': {'picture_name': 'pic.jpg'}}
        """
        case_id = str2int(case_id)
        args = CASETaskPost.parse_args()
        mode_id = args['mode_id']
        form_data = request.form
        file_data = request.files
        result = CaseTaskService.create(case_id=case_id, mode_id=mode_id, form_data=form_data, file_data=file_data)
        return jsonify(Response.correct(data=result))
