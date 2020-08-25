#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/28 15:34
# @Author : wangweimin
# @File   : r_model_description.py
# @Desc   : 无用

# Todo
# 模型信息
# 未实现

from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.models import Model, ModelInfo, ModelVersion, ModelSourceCode

ModelPost = reqparse.RequestParser()
ModelPost.add_argument('project_id', required=True, type=int, location='form')
ModelPost.add_argument('model_name', required=True, type=str, location='form')
ModelPost.add_argument('description', type=str, location='form')


class ModelDescription(Resource):

    def get(self, model_id: str):
        """
        获取已存储模型源码
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
              {'message': {'ValueError': 'Error model id'}， 'code': 1}
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
        res = dict()
        model: Model = Model.query.get(int(model_id))
        if model is None:
            res.update(message={'Error': 'Error model id by model source code'}, code=1)
        else:
            try:
                model_version: ModelVersion = model.model_version.first()
                model_src: ModelSourceCode = model_version.model_source_code
                src = DataFileOperator(address='src').get(filename=model_src.alias)
                res.update(data=src, code=0)
            except Exception as e:
                res.update(message={'Error': str(e)}, code=1)
        return jsonify(res)

    def put(self, model_id: str):
        """
        提交模型源码
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
        pass
