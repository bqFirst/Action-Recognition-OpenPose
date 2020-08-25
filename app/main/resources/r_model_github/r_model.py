#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/1/9 0009 11:12
# @Author : wangw
# @File   : r_model.py
# @Desc   :

from flask import jsonify, send_from_directory
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.model_operator.model_description_operator import ModelDesService
from app.main.services.operator.model_operator.model_operator import ModelService
from app.main.services.operator.model_operator.model_src_operator import ModelSrcService
from app.models import User

from app.main.services.operator.model_operator_github.model_operator import ModelTfService


ModelPost = reqparse.RequestParser()
ModelPost.add_argument('project_id', required=True, type=int, location='form')
ModelPost.add_argument('model_name', required=True, type=str, location='form')
ModelPost.add_argument('description', required=False, type=str, location='form')
ModelPost.add_argument('path', type=str, required=False, location='form')
ModelPost.add_argument('shell', type=list, required=False, location='form')


class MODELGithub(Resource):

    @error_handler
    def post(self):
        """
        创建模型
        ---
        tags:
          - Github模型
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
          - name: path
            in: formData
            type: String
            required: false
            description: 需要上传的文件夹的路径
          - name: shell
            in: formData
            type: list
            description: shell命令
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
        path = args['path']
        shell = args['shell']
        # model_id = args['model_id']
        user_id = User.query.first().id
        model_id: int = ModelTfService.create_github(project_id=project_id, model_name=model_name, user_id=user_id,
                                                     path=path, description=description, shell=shell)
        return jsonify(Response.correct(model_id=model_id))


ModelOperatorPut = reqparse.RequestParser()
ModelOperatorPut.add_argument('model_name', type=str, location='form')
ModelOperatorPut.add_argument('description', type=str, location='form')

ModelOperatorPost = reqparse.RequestParser()
ModelOperatorPost.add_argument('output_node_names', required=False, type=str, location='form')


class MODELOperatorGithub(Resource):

    @error_handler
    def post(self, model_id: str):
        """
        运行、训练模型
        ---
        tags:
          - Github模型
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
            ckpt_dir: str = ModelTfService.train(model_id=model_id)

            # status: bool = ModelTfService.save(model_id=model_id, pipe=ckpt_dir, output_node_names=out)
            if ckpt_dir:
                res.update(Response.correct())
            else:
                res.update(Response.error(message={'Error': 'Train Error'}))
        except Exception as e:
            res.update(Response.error(message={'Error': str(e)}))
        return jsonify(res)


