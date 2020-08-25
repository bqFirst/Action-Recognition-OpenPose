#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/3 11:14
# @Author : wangweimin
# @File   : r_task.py
# @Desc   :

from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.resources.resources_config import PermitApplicationSrcType
from app.main.services.operator.task_operator.task_operator import TaskService
from app.models import User

TASKPost = reqparse.RequestParser()
TASKPost.add_argument('data_link_id', required=True, type=int, location='form')
TASKPost.add_argument('task_name', required=True, type=str, location='form')
TASKPost.add_argument('application_id', required=True, type=int, location='form')
TASKPost.add_argument('description', type=str, location='form')
TASKPost.add_argument('data_type', required=True, type=str, location='form', choices=PermitApplicationSrcType)
TASKPost.add_argument('model_id', required=True, type=int, location='form')


class TASK(Resource):

    @error_handler
    def post(self):
        """
        新建离线任务
        ---
        tags:
          - 离线任务
        parameters:
          - name: task_name
            in: formData
            type: string
            required: true
            description: 任务名称
          - name: application_id
            in: formData
            type: integer
            required: true
            description: 应用id
          - name: data_link_id
            in: formData
            type: integer
            required: true
            description: 被预测数据id
          - name: data_type
            in: formData
            required: true
            description: 数据链接的类型，'csv'、'excel'、'MySQL'、'picture'等
            schema:
              type: string
              enum:
                - csv
                - excel
          - name: description
            in: formData
            type: string
          - name: model_id
            in: formData
            type: integer
            required: true
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
              {'code': 1, 'message': {'ValueError': 'name repeated'}}
          200:
            description: 新建成功
            schema:
              properties:
                task_id:
                  type: integer
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'task_id': 1}
        """
        args = TASKPost.parse_args()
        description: str = args['description'] or ''
        task_name: str = args['task_name']
        data_link_id: int = args['data_link_id']
        application_id = args['application_id']
        data_type = args['data_type']
        user_id = User.query.first().id
        model_id: int = args['model_id']
        task_id = TaskService.create(description=description, task_name=task_name, data_link_id=data_link_id,
                                     data_type=data_type, application_id=application_id, model_id=model_id,
                                     user_id=user_id)
        return jsonify(Response.correct(task_id=task_id))


class TaskOperator(Resource):

    def unused_put(self, task_id: str):
        """
        修改任务信息
        ---
        tags:
          - 离线任务
        parameters:
          - name: task_id
            in: path
            type: integer
            required: true
            description: 应用id
          - name: name
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
            examples:
              {'message': {'ValueError': 'Error task id'}}
          200:
            description: 修改成功
            schema:
              properties:
                status:
                  type: string
            examples:
              {'status': 'success'}
        """
        pass

    @error_handler
    def delete(self, task_id: str):
        """
        删除任务
        ---
        tags:
          - 离线任务
        parameters:
          - name: task_id
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
              {'message': {'ValueError': 'Error task id'}, 'code': 1}
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
        task_id = str2int(task_id)
        TaskService.delete(task_id=task_id)
        return jsonify(Response.correct())

    def unused_get(self, task_id):
        """
        获取任务信息
        ---
        tags:
          - 离线任务
        parameters:
          - name: task_id
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
            examples:
              {'message': {'ValueError': 'Error task id'}}
          200:
            description: 任务信息
            schema:
              properties:
                task_id:
                  type: integer
                task_name:
                  type: string
                description:
                  type: string
            examples:
              {'task_id_id': 1, 'task_id_name': 't1', 'description': '2019绩效考核任务'}
        """
        pass


TaskControllerPut = reqparse.RequestParser()
TaskControllerPut.add_argument('operator', required=True, type=int, location='form', choices=(0, 1, ))


class TaskController(Resource):

    @error_handler
    def put(self, task_id: str):
        """
        任务启动与停止(暂无停止操作)
        ---
        tags:
          - 离线任务
        parameters:
          - name: task_id
            in: path
            type: integer
            required: true
          - name: operator
            in: formData
            type: integer
            required: True
            description: 1代表启动，0代表停止
        responses:
          500:
            description: 操作失败
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
              {'message': {'ValueError': 'Error task id'}, 'code': 1}
          200:
            description: 操作成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0}
        """
        args = TaskControllerPut.parse_args()
        task_id = str2int(task_id)
        operator = args['operator']
        if 1 == operator:
            TaskService.restart(task_id=task_id)
        elif 0 == operator:
            # TaskService.stop(task_id=task_id)
            raise TypeError
        return jsonify(Response.correct())
