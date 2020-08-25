#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/2/24 16:06
# @Author : wangweimin
# @File   : r_human_intrusion.py
# @Desc   :


from flask import jsonify
from flask_restful import Resource

from app.main.resources.r_base.resources_response import Response

from app.main.resources.r_base.r_aop.error_handler import error_handler

from app.main.services.operator.case_demo_operator.human_intrusion_operator import CaseHumanIntrusionDemoService


class HumanIntrusionData(Resource):

    @error_handler
    def get(self):
        """
        获取人员入侵信息
        ---
        tags:
          - 案例demo
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
              {'message': {'ValueError': 'Error status id'}, 'code': 1}
          200:
            schema:
              properties:
                data:
                  area:
                    type: array
                    items:
                      - name: area_name
                      - name: child
                        type: array
                        items:
                          - name: camera_address
                            type: string
                          - name: key
                            type: string
                  camera:
                    type: array
                    items:
                      - name: video
                        type: string
                      - name: camera_address
                        type: string
                      - name: key
                        type: string
                      - name: alarm_info
                        type: array
                        items:
                          - name: alarm_time
                            type: integer
                          - name: alarm_content
                            type: string
                code:
                  type: integer
                  default: 0
            examples:
              {'data': {'camera' : [{'video': '/case_demo/video.avi', 'key': '1', 'camera_address': '办公室-物流办公室', 'alarm_info': [{'alarm_time': 34, 'alarm_content': '发现2名人员入侵'}, {'alarm_time': 131, 'alarm_content': '发现1名人员入侵'}]}], 'area': [{'area_name': '办公室', 'child': [{'camera_address': '物流办公室', 'key': '1'}]}]}, 'code': 0}
        """
        intrusion_data = CaseHumanIntrusionDemoService.get()
        return jsonify(Response.correct(**intrusion_data))
