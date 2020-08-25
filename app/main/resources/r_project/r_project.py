#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/2 17:31
# @Author : wangweimin
# @File   : r_project.py
# @Desc   :

from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.project_operator.project_operator import ProjectService
from app.main.services.operator.project_operator.project_edit_window_operator import ProjectEditWindowService
from app.models import User

ProjectPost = reqparse.RequestParser()
ProjectPost.add_argument('catalog_id', required=True, type=int, location='form')
ProjectPost.add_argument('description', type=str, location='form')
ProjectPost.add_argument('project_name', required=True, type=str, location='form')
ProjectPost.add_argument('data_links_id', action='append', location='form', type=int)


class PROJECT(Resource):

    @error_handler
    def post(self):
        """
        新建工程
        ---
        tags:
          - 工程
        parameters:
          - name: project_name
            in: formData
            type: string
            required: true
            description: 工程名称
          - name: catalog_id
            in: formData
            type: integer
            required: true
            description: 工程目录id
          - name: description
            in: formData
            type: string
            description: 工程描述
          - name: data_links_id
            in: formData
            type: array
            items:
              type: integer
            description: 管理数据源链接id，以str形式传递，多个id同样以多个data_links_id传递(0.3版本后取消无需传递)
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
            description: 创建成功
            schema:
              properties:
                project_id:
                  type: integer
                code:
                  type: integer
                  default: 0
            examples:
              {'project_id': 1, 'code': 0}
        """
        args = ProjectPost.parse_args()
        description: str = args['description'] or ''
        project_name: str = args['project_name']
        data_links_id: list = args['data_links_id'] or []
        user_id = User.query.first().id
        catalog_id: int = args['catalog_id']
        project_id = ProjectService.create(project_name=project_name, description=description, user_id=user_id,
                                           data_links_id=data_links_id, catalog_id=catalog_id)
        return jsonify(Response.correct(project_id=project_id))


ProjectOperatorPut = reqparse.RequestParser()
ProjectOperatorPut.add_argument('project_name', type=str, location='form', required=True)


class ProjectOperator(Resource):

    @error_handler
    def put(self, project_id: str):
        """
        修改工程名称
        ---
        tags:
          - 工程
        parameters:
          - name: project_id
            in: path
            type: integer
            required: true
            description: 工程id
          - name: project_name
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
              {'message': {'ValueError': 'Error project id'}, 'code': 1}
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
        args = ProjectOperatorPut.parse_args()
        project_name = args['project_name']
        project_id = str2int(project_id)
        ProjectService.rename(project_id=project_id, project_name=project_name)
        return jsonify(Response.correct())

    @error_handler
    def delete(self, project_id: str):
        """
        删除工程
        ---
        tags:
          - 工程
        parameters:
          - name: project_id
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
              {'message': {'ValueError': 'models in such project id'}, 'code': 1}
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
        project_id = str2int(project_id)
        ProjectService.delete(project_id=project_id)
        return jsonify(Response.correct())

    @error_handler
    def get(self, project_id):
        """
        获取工程信息
        ---
        tags:
          - 工程
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
            description: 工程信息
            schema:
              properties:
                project_id:
                  type: integer
                project_name:
                  type: string
                creator:
                  type: string
                create_time:
                  type: string
                catalog_name:
                  type: string
                  description: 所属工程目录名称
                description:
                  type: string
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'project_id': 1, 'project_name': 'myProject', 'creator': 'me', 'create_time': '2019-01-01 00:00:00', 'catalog_name': 'projectCatalog', 'description': 'a'}
        """
        project_id = str2int(project_id)
        res: dict = ProjectService.get(project_id=project_id)
        res.update(Response.correct())
        return jsonify(res)


PROJECTEditWindowPut = reqparse.RequestParser()
PROJECTEditWindowPut.add_argument('model_name', type=str, location='form', required=True)
PROJECTEditWindowPut.add_argument('description', type=str, location='form', required=True)
PROJECTEditWindowPut.add_argument('src', type=str, location='form', required=True)
PROJECTEditWindowPut.add_argument('data_format', type=str, location='form', required=True)


class PROJECTEditWindow(Resource):

    @error_handler
    def get(self, project_id: str):
        """
        获取工程编辑窗口信息
        ---
        tags:
          - 工程
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
            examples:
              {'message': {'ValueError': 'Error project id'}, 'code': 1}
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
              {'model_name': 'model', 'description': '随便', 'model_id': 0, 'src': 'from', 'code': 0}
        """
        project_id = str2int(project_id)
        data = ProjectEditWindowService.get(project_id=project_id)
        return jsonify(Response.correct(**data))

    @error_handler
    def put(self, project_id: str):
        """
        保存工程编辑窗口信息
        ---
        tags:
          - 工程
        parameters:
          - name: project_id
            in: path
            type: integer
            required: true
            description: 工程id
          - name: model_name
            in: formData
            type: string
          - name: description
            in: formData
            type: string
          - name: src
            in: formData
            type: string
          - name: data_format
            in: formData
            type: string
            description: 数据应用格式
        responses:
          500:
            description: 保存失败
            schema:
              properties:
                message:
                  items:
                    - name: Error
                      type: string
                code:
                  type: integer
            examples:
              {'message': {'ValueError': 'Error project id'}, 'code': 1}
          200:
            description: 保存成功
            schema:
              properties:
                code:
                  type: integer
            examples:
              {'code': 0}
        """
        args = PROJECTEditWindowPut.parse_args()
        model_name = args['model_name']
        description = args['description']
        data_format = args['data_format']
        src = args['src']
        project_id = str2int(project_id)
        ProjectEditWindowService.save(project_id=project_id, model_name=model_name, description=description,
                                      src=src, data_format=data_format)
        return jsonify(Response.correct())
