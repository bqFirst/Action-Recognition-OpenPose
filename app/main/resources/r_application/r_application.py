#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/3 10:48
# @Author : wangweimin
# @File   : r_application.py
# @Desc   :

from flask import jsonify, send_from_directory
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.application_operator.application_operator import ApplicationService
from app.main.services.operator.application_operator.application_task_operator import ApplicationTaskService
from app.models import User

ApplicationPost = reqparse.RequestParser()
ApplicationPost.add_argument('models_id', required=True, type=int, location='form', action='append')
ApplicationPost.add_argument('application_name', required=True, type=str, location='form')
ApplicationPost.add_argument('catalog_id', required=True, type=int, location='form')
ApplicationPost.add_argument('description', type=str, location='form')


class APPLICATION(Resource):

    @error_handler
    def post(self):
        """
        新建应用
        ---
        tags:
          - 应用
        parameters:
          - name: application_name
            in: formData
            type: string
            required: true
            description: 应用名称
          - name: catalog_id
            in: formData
            type: integer
            required: true
            description: 应用目录id
          - name: description
            in: formData
            type: string
          - name: models_id
            in: formData
            type: array
            required: True
            description: 应用所使用的模型id
            items:
              type: integer
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
              {'code': 1, 'message': {'ValueError': 'name repeated'}}
          200:
            description: 创建成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                application_id:
                  type: integer
            examples:
              {'code': 0, 'application_id': 1}
        """
        args = ApplicationPost.parse_args()
        models_id = args['models_id']
        application_name = args['application_name']
        catalog_id = args['catalog_id']
        user_id = User.query.first().id
        application_id = ApplicationService.create(catalog_id=catalog_id, models_id=models_id,
                                                   application_name=application_name, user_id=user_id)
        return jsonify(Response.correct(application_id=application_id))


ApplicationOperatorPut = reqparse.RequestParser()
ApplicationOperatorPut.add_argument('application_name', required=True, type=str, location='form')
ApplicationOperatorPut.add_argument('description', type=str, location='form')


class ApplicationOperator(Resource):

    @error_handler
    def put(self, application_id: str):
        """
        修改应用名称或描述信息
        ---
        tags:
          - 应用
        parameters:
          - name: application_id
            in: path
            type: integer
            required: true
            description: 应用id
          - name: application_name
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
              {'code': 1, 'message': {'ValueError': 'Error application id'}}
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
        application_id = str2int(application_id)
        args = ApplicationOperatorPut.parse_args()
        application_name = args['application_name']
        description = args['description']
        ApplicationService.rename(application_id=application_id, application_name=application_name)
        return jsonify(Response.correct())

    @error_handler
    def delete(self, application_id: str):
        """
        删除应用
        ---
        tags:
          - 应用
        parameters:
          - name: application_id
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
              {'code': 1, 'message': {'ValueError': 'there are tasks in such application'}}
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
        application_id = str2int(application_id)
        ApplicationService.delete(application_id=application_id)
        return jsonify(Response.correct())

    @error_handler
    def get(self, application_id):
        """
        获取应用信息
        ---
        tags:
          - 应用
        parameters:
          - name: application_id
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
              {'code': 1, 'message': {'ValueError': 'Error application id'}}
          200:
            description: 应用信息
            schema:
              properties:
                data:
                  type: array
                  items:
                    - name: application_id
                      type: integer
                    - name: application_name
                      type: string
                    - name: creator
                      type: string
                    - name: create_time
                      type: string
                    - name: status_id
                      type: integer
                      description: 1服务中，2未启动，3启动中，4停止中
                    - name: status_name
                      type: string
                    - name: image_status_id
                      type: integer
                      description: 1未打包，2打包中，3打包成功
                    - name: image_status_name
                      type: string
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'data': {'application_id': 1, 'application_name': 'app1', 'creator': 'me', 'create_time': '2019-01-01 00:00:00', 'status_id': 1, 'status_name': '服务中', 'image_status_id': 1, 'image_status_name': '未打包'}}
        """
        application_id = str2int(application_id)
        data = ApplicationService.get(application_id=application_id)
        return jsonify(Response.correct(data=data))


ApplicationTaskPost = reqparse.RequestParser()
ApplicationTaskPost.add_argument('status_id', type=int, location='form')


class ApplicationTask(Resource):

    @error_handler
    def get(self, application_id: str):
        """
        获取应用及其下离线任务信息
        ---
        tags:
          - 应用
        parameters:
          - name: application_id
            in: path
            type: integer
            required: true
          - name: status_id
            in: query
            type: integer
            default: 0
            description: 任务过滤，0表示全部
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
              {'code': 1, 'message': {'ValueError': 'Error project id'}}
          200:
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                data:
                  type: array
                  items:
                    - name: task_id
                      type: integer
                    - name: task_name
                      type: string
                    - name: status_id
                      type: integer
                    - name: creator
                      type: string
                    - name: status_name
                      type: string
                    - name: run_time
                      type: string
                    - name: predicted_data_name
                      type: string
                    - name: predicted_data_id
                      type: integer
                    - name: data_type
                      type: string
                    - name: result_data_id
                      type: integer
                      description: 0表示任务未执行成功
                    - name: result_data_name
                      type: string
                    - name: task_log_id
                      type: integer
                      description: 日志id
            examples:
              {'code': 0, 'data': [{'predicted_data_id': 1, 'data_type': 'csv', 'creator': 'm', 'task_id': 1, 'task_name': 't1', 'status_name': '运行成功', 'status_id': 1, 'run_time': '2019-01-01 00:00:00', 'predicted_data_name': '2019绩效.csv', 'result_data_id': 1, 'result_data_name': '结果.csv'}, ]}
        """
        application_id = str2int(application_id)
        args = ApplicationTaskPost.parse_args()
        status_id = args['status_id'] or 0
        data = ApplicationTaskService.get(application_id=application_id, status_id=status_id)
        return jsonify(Response.correct(data=data))


class ApplicationDownload(Resource):

    @error_handler
    def put(self, application_id: str):
        """
        打包应用
        ---
        tags:
          - 应用
        parameters:
          - name: application_id
            in: path
            type: integer
            required: true
            description: 应用id
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
              {'message': {'ValueError': 'Error application id'}, 'code': 1}
          200:
            description: 打包成功
        """
        application_id = str2int(application_id)
        ApplicationService.package(application_id=application_id, error=False)
        return jsonify(Response.correct())

    @error_handler
    def get(self, application_id: str):
        """
        下载应用（包含docker镜像与模型说明）
        ---
        tags:
          - 应用
        parameters:
          - name: application_id
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
        application_id = str2int(application_id)
        directory, file, filename = ApplicationService.download(application_id=application_id, error=False)
        return send_from_directory(directory=directory, filename=file, as_attachment=True,
                                   attachment_filename=filename)


ApplicationControllerPost = reqparse.RequestParser()
ApplicationControllerPost.add_argument('operator', required=True, type=int, location='form', choices=(0, 1, ))


class ApplicationController(Resource):

    @error_handler
    def put(self, application_id: str):
        """
        应用启动与关闭
        ---
        tags:
          - 应用
        parameters:
          - name: application_id
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
              {'message': {'ValueError': 'Error application id'}, 'code': 1}
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
        args = ApplicationControllerPost.parse_args()
        application_id = str2int(application_id)
        operator = args['operator']
        if 1 == operator:
            ApplicationService.start(application_id=application_id)
        elif 0 == operator:
            ApplicationService.stop(application_id=application_id)
        return jsonify(Response.correct())
