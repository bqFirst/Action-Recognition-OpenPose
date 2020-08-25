#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/2 19:29
# @Author : wangweimin
# @File   : r_model.py
# @Desc   :

from flask import jsonify, send_from_directory
from flask_restful import Resource, reqparse
from sklearn.pipeline import Pipeline

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.model_operator.model_description_operator import ModelDesService
from app.main.services.operator.model_operator.model_operator import ModelService
from app.main.services.operator.model_operator.model_src_operator import ModelSrcService
from app.models import User

ModelPost = reqparse.RequestParser()
ModelPost.add_argument('project_id', required=True, type=int, location='form')
ModelPost.add_argument('model_name', required=True, type=str, location='form')
ModelPost.add_argument('description', required=True, type=str, location='form')
# ModelPost.add_argument('model_id', type=int, location='form')
ModelPost.add_argument('src', type=str, required=True, location='form')


class MODEL(Resource):

    @error_handler
    def post(self):
        """
        生成模型
        ---
        tags:
          - 模型
        parameters:
          - name: model_name
            in: formData
            type: string
            required: true
            description: 模型名称
          - name: project_id
            in: formData
            type: integer
            required: true
            description: 工程id
          - name: description
            in: formData
            type: string
            description: 模型备注信息，若用户无填写，提交空字符串
          - name: src
            in: formData
            type: string
            required: true
            description: 模型源码
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
              {'message': {'ValueError': 'name repeated'}, 'code': 1}
          200:
            description: code为0表示创建成功，code为7代表验证出错，并附带验证错误信息
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                model_id:
                  type: integer
                message:
                  type: string
            examples:
              {'code': 0, 'model_id': 1}
        """
        args = ModelPost.parse_args()
        model_name = args['model_name']
        project_id = args['project_id']
        description = args['description']
        src = args['src']
        # model_id = args['model_id']
        user_id = User.query.first().id
        result: str = ModelSrcService.verify(src=src)
        if not result:
            model_id: int = ModelService.create(project_id=project_id, model_name=model_name, user_id=user_id, src=src,
                                                description=description)
            return jsonify(Response.correct(model_id=model_id))
        else:
            return jsonify(Response.popup_error(message=result))


ModelOperatorPut = reqparse.RequestParser()
ModelOperatorPut.add_argument('model_name', type=str, location='form')
ModelOperatorPut.add_argument('description', type=str, location='form')

ModelOperatorPost = reqparse.RequestParser()
ModelOperatorPost.add_argument('output_node_names', required=False, type=str, location='form')


class MODELOperator(Resource):

    @error_handler
    def unused_put(self, model_id: str):
        """
        修改模型名称或备注信息（暂不使用）
        ---
        tags:
          - 模型
        parameters:
          - name: model_id
            in: path
            type: integer
            required: true
            description: 模型id
          - name: model_name
            in: formData
            type: string
          - name: description
            in: formData
            type: string
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
              {'message': {'ValueError': 'Error model id'}, 'code': 1}
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
        args = ModelOperatorPut.parse_args()
        model_name = args['model_name']
        description = args['description']
        try:
            model_id = str2int(model_id)
            if model_name is not None:
                ModelService.rename(model_id=model_id, model_name=model_name)
            if description is not None:
                ModelDesService.modify(model_id=model_id, description=description)
            return jsonify(Response.correct())
        except Exception as e:
            return jsonify(Response.error(message={'Error': str(e)}))

    @error_handler
    def delete(self, model_id: str):
        """
        删除模型
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
              {'message': {'Error': 'Error model id'}, 'code': 1}
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
        ModelService.delete(model_id=str2int(model_id))
        return jsonify(Response.correct())

    @error_handler
    def unused_post(self, model_id: str):
        """
        运行、训练模型（暂不使用）
        ---
        tags:
          - 模型
        parameters:
          - name: model_id
            in: path
            type: integer
            required: true
            description: 模型id
          - name: output_node_names
            in: formData
            type: string
            description: 神经网络保存node
        responses:
          500:
            description: 运行失败（可能不返回状态）
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
            description: 运行成功（可能不返回状态）
            schema:
              properties:
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0}
        """
        res = dict()
        args = ModelOperatorPost.parse_args()
        out = args['output_node_names']
        try:
            model_id = str2int(model_id)
            pipe: Pipeline = ModelService.train(model_id=model_id)
            status: bool = ModelService.save(model_id=model_id, pipe=pipe, output_node_names=out)
            if status:
                res.update(Response.correct())
            else:
                res.update(Response.error(message={'Error': 'Train Error'}))
        except Exception as e:
            res.update(Response.error(message={'Error': str(e)}))
        return jsonify(res)

    @error_handler
    def get(self, model_id: str):
        """
        获取模型信息
        ---
        tags:
          - 模型
        parameters:
          - name: model_id
            in: path
            type: integer
            required: true
            description: 模型id
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
            schema:
              properties:
                model_name:
                  type: string
                description:
                  type: string
                model_id:
                  type: integer
                src:
                  type: string
                code:
                  type: integer
                data_format:
                  type: str
            examples:
              {'model_name': 'model', 'description': '随便', 'model_id': 1, 'src': 'from', 'code': 0}
        """
        # user_id = User.query.first().id
        model_id = str2int(model_id)
        data = ModelService.get(model_id=model_id)
        return jsonify(Response.correct(**data))


class ModelDownload(Resource):

    @error_handler
    def get(self, model_id: str):
        """
        下载模型（包含docker镜像与模型说明）
        ---
        tags:
          - 模型
        parameters:
          - name: model_id
            in: path
            type: integer
            required: true
            description: 模型id
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
              {'message': {'ValueError': 'Error model id'}, 'code': 1}
          200:
            description: 下载成功
        """
        user_id = User.query.first().id
        model_id = str2int(model_id)
        directory, file, filename = ModelService.download(model_id=model_id, user_id=user_id, error=False)
        return send_from_directory(directory=directory, filename=file, as_attachment=True,
                                   attachment_filename=filename)

    @error_handler
    def put(self, model_id: str):
        """
        打包模型
        ---
        tags:
          - 模型
        parameters:
          - name: model_id
            in: path
            type: integer
            required: true
            description: 模型id
        responses:
          500:
            description: 打包失败
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
            description: 打包成功
        """
        user_id = User.query.first().id
        model_id = str2int(model_id)
        status: bool = ModelService.package(model_id=model_id, user_id=user_id)
        if status:
            return jsonify(Response.correct())
        return jsonify(Response.error(message={'Error': "未知错误"}))
