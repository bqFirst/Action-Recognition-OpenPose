#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/15 10:21
# @Author : wangweimin
# @File   : r_picture.py
# @Desc   : 无用

from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.picture_operator.picture_operator import PictureService


class PICTURE(Resource):

    def get(self, picture_id: str):
        """
        获取原始图片信息（暂时无用）
        ---
        tags:
          - 图片
        parameters:
          - name: picture_id
            in: path
            required: true
            type: integer
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
              {'message': {'ValueError': 'Error picture id'}, 'code': 1}
          200:
            description: 获取图片
            schema:
              properties:
                original_url:
                  type: string
                picture_name:
                  type: string
                picture_id:
                  type: integer
                label_name:
                  type: array
                  items:
                    type: sting
                code:
                  type: integer
                  default: 0
            example:
              {'code': 0, 'original_url': '....', 'picture_name': '2019a.jpg', 'picture_id': 1, 'label_name': ['normal']}
        """
        try:
            picture_id = str2int(picture_id)
            result = PictureService.get(picture_id=picture_id)
            return jsonify(Response.correct(**result))
        except Exception as e:
            return jsonify(Response.error(message={'Error': str(e)}))
