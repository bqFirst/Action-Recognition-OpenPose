#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/1/6 14:50
# @Author : wangweimin
# @File   : r_docker_image.py
# @Desc   :


from flask import jsonify, send_from_directory
from flask_restful import Resource

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.docker_operator.docker_image_operator import DockerBaseImageService


class DOCKERBaseImage(Resource):

    @error_handler
    def get(self):
        """
        获取基础docker镜像信息
        ---
        tags:
          - docker
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
              {'message': {'ValueError': 'Something Error'}, 'code': 1}
          200:
            description: 获取成功
            schema:
              properties:
                data:
                  type: array
                  items:
                    - name: docker_image_id
                      type: integer
                    - name: docker_image_name
                      type: string
                code:
                  type: integer
                  default: 0
            examples:
              {'data': {'docker_image_id': 1, 'docker_image_name': 'flask-sklearn'}, 'code': 0}
        """
        result = DockerBaseImageService.base_image_info()
        return jsonify(Response.correct(data=result))


class DOCKERBaseImageDownload(Resource):

    @error_handler
    def get(self, docker_image_id: str):
        """
        下载基础docker镜像
        ---
        tags:
          - docker
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
              {'message': {'ValueError': 'Error base image id'}, 'code': 1}
          200:
            description: 下载成功
        """
        docker_image_id = str2int(docker_image_id)
        directory, file, filename = DockerBaseImageService.download(docker_image_id=docker_image_id)
        return send_from_directory(directory=directory, filename=file, as_attachment=True,
                                   attachment_filename=filename)
