#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/2 9:38
# @Author : wangweimin
# @File   : r_task_log.py
# @Desc   :

from flask import jsonify
from flask_restful import Resource

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.task_operator.task_log_operator import TaskLogService


class TaskLogOperator(Resource):

    @error_handler
    def get(self, task_log_id):
        """
        获取任务日志信息
        ---
        tags:
          - 离线任务数据
        parameters:
          - name: task_log_id
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
              {'code': 1, 'message': {'ValueError': 'Error log id'}}
          200:
            description: 获取成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                data:
                  type: string
                task_name:
                  type: string
            examples:
              {'code': 0, 'data': '.....', 'task_name': 'myTask'}
        """
        task_log_id = str2int(task_log_id)
        data = TaskLogService.get(task_log_id)
        return jsonify(Response.correct(**data))
