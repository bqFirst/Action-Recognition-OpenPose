#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/23 11:16
# @Author : wangweimin
# @File   : r_model_src.py
# @Desc   :

from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.model_operator.model_src_operator import ModelSrcService
from app.models import User


MODELSrcPut = reqparse.RequestParser()
MODELSrcPut.add_argument('src', type=str, required=True, location='form')


class MODELSrc(Resource):

    @error_handler
    def get(self, model_id: str):
        """
        获取模型源码
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
                  type: string
                  description: 源码
                code:
                  type: integer
                  default: 0
            examples:
              {'data': 'import pandas as pd', 'code': 0}
        """
        model_id = str2int(model_id)
        data = ModelSrcService.get(model_id=model_id)
        return jsonify(Response.correct(data=data))

    def unused_put(self, model_id: str):
        """
        提交模型源码（暂不使用）
        ---
        tags:
          - 模型
        parameters:
          - name: model_id
            in: path
            type: integer
            required: true
          - name: src
            in: formData
            type: string
            required: true
            description: 模型源码
        responses:
          500:
            description: 提交失败
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
            description: 提交成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0}
        """
        model_id: int = int(model_id)
        args = MODELSrcPut.parse_args()
        src: str = args['src']
        user_id = User.query.first().id
        try:
            # model_src_preserve_service(model_id=model_id, user_id=user_id, new_src=src)
            return jsonify(Response.correct())
        except Exception as e:
            return jsonify(Response.error(message={'Error': str(e)}))

    def unused_delete(self, model_id: str):
        """
        重置源码至初始阶段（暂不使用）
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
            description: 重置失败
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
            description: 获取初始源码
            schema:
              properties:
                data:
                  type: string
                  description: 源码
                code:
                  type: integer
                  default: 0
            examples:
              {'data': 'import pandas as pd', 'code': 0}
        """
        try:
            # src = model_src_reset_service(model_id=int(model_id))
            return jsonify(Response.correct())  # data=src
        except Exception as e:
            return jsonify(Response.error(message={'Error': str(e)}))


ModelSrcVerifyPut = reqparse.RequestParser()
ModelSrcVerifyPut.add_argument('src', type=str, required=True, location='form')


class MODELSrcVerify(Resource):

    @error_handler
    def put(self):
        """
        模型代码验证
        ---
        tags:
          - 模型
        parameters:
          - name: src
            in: formData
            type: string
            required: true
            description: 模型源码
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
              {'message': {'ValueError': 'Error model id'}, 'code': 1}
          200:
            description: code为0表示验证成功，并返回验证结果，code为7代表验证出错，并附带验证错误信息
            schema:
              properties:
                message:
                  type: string
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 7, 'message': ['....']}
        """
        args = ModelSrcVerifyPut.parse_args()
        src: str = args['src']
        result: str = ModelSrcService.verify(src=src)
        if not result:
            return jsonify(Response.correct())
        else:
            return jsonify(Response.popup_error(message=result))
