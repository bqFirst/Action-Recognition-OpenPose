#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/23 11:17
# @Author : wangweimin
# @File   : r_model_info.py
# @Desc   :

from flask import jsonify
from flask_restful import Resource

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.model_operator.model_info_operator import ModelInfoService


class MODELInfo(Resource):

    @error_handler
    def get(self, model_id: str):
        """
        获取自定义模型信息
        ---
        tags:
          - 模型
        parameters:
          - name: model_id
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
              {'message': {'ValueError': 'Error model id'}, 'code': 1}
          200:
            description: 获取成功
            schema:
              properties:
                data:
                  description: 用户自定义模型信息，为mapping
                  items:
                    - name: properties
                      description: 用户自定义模型信息示例
                code:
                  type: integer
                  default: 0
            examples:
              {'data': {'properties': 0.981}, 'code': 0}
        """
        model_id = str2int(model_id)
        info = ModelInfoService.get(model_id=model_id)
        return jsonify(Response.correct(data=info))
