#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/3/3 0003 18:51
# @Author : wangw
# @File   : r_baidu_map_2_mysql.py
# @Desc   :

from flask import jsonify
from flask_restful import Resource

from app.main.resources.r_base.r_aop.error_handler import error_handler

from app.main.services.operator.baidu_map_opterator.baidu_map import BaiduMap

from flask import jsonify
from flask_restful import Resource

from app.main.resources.r_base.resources_response import Response

from app.main.resources.r_base.r_aop.error_handler import error_handler


class MAP2MYSQL(Resource):
    @error_handler
    def get(self):
        """
        摄像头分布信息入库个人测试，代码不提交
        ---
        tags:
          - 摄像头分布信息入库
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
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0}
        """
        res = BaiduMap.get()
        return jsonify(Response.correct(**res))