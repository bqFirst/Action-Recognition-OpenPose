#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/2/24 15:54
# @Author : wangweimin
# @File   : r_camera_monitor.py
# @Desc   :

from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.resources_response import Response

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.services.operator.case_demo_operator.camera_monitor_operator import CaseCameraMonitorDemoService


class CameraMonitorDistribution(Resource):

    @error_handler
    def get(self):
        """
        获取摄像头分布信息
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
              {'message': {'ValueError': 'Error'}, 'code': 1}
          200:
            schema:
              properties:
                data:
                  type: array
                  items:
                   - name: city
                     type: string
                   - name: city_id
                     type: integer
                   - name: amount
                     type: integer
                   - name: districts
                     type: array
                     items:
                       - name: district
                         type: string
                       - name: district_id
                         type: integer
                       - name: amount
                         type: integer
                       - name: streets
                         type: array
                         items:
                           - name: longitude
                             type: float
                           - name: latitude
                             type: float
                           - name: address
                             type: string
                           - name: amount
                             type: integer
                code:
                  type: integer
                  default: 0
            examples:
              {'data' : [{'city': '广州市', 'city_id': 1, 'amount': 4644, 'districts': [{'district': '天河区', 'district_id': 1, 'amount': 213, 'strees': [{'longitude': 23.1, 'latitude': 87, 'address': '中山大道', 'amount': 23}]}]}], 'code': 0}
        """
        # CaseCameraMonitorDemoService().map_to_mysql()
        distribution = CaseCameraMonitorDemoService.distribution()
        return jsonify(Response.correct(data=distribution))


CameraMonitorDataGet = reqparse.RequestParser()
CameraMonitorDataGet.add_argument('status_id', type=int, required=True, location='args')


class CameraMonitorData(Resource):

    @error_handler
    def get(self):
        """
        获取摄像头检测图片信息
        ---
        tags:
          - 案例demo
        parameters:
          - name: status_id
            in: query
            type: integer
            required: true
            description: 检测状态
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
                  type: array
                  items:
                   - name: normal_picture
                     type: integer
                   - name: current_picture
                     type: integer
                   - name: status_name
                     type: string
                   - name: camera_type
                     type: string
                   - name: camera_businesses
                     type: string
                   - name: camera_businesses_telephone
                     type: string
                   - name: camera_ip
                     type: string
                code:
                  type: integer
                  default: 0
            examples:
              {'data' : {'normal_picture': '/simulation/picture1.jpg', 'current_picture': '/simulation/picture2.jpg', 'status_name': '异常（偏移）', 'camera_businesses': '广州大华', 'camera_businesses_telephone': '020-83217324', 'camera_ip': '207.183.59.59'}, 'code': 0}
        """
        args = CameraMonitorDataGet.parse_args()
        status_id = args['status_id']
        demo_data = CaseCameraMonitorDemoService.get(status_id)
        return jsonify(Response.correct(data=demo_data))
