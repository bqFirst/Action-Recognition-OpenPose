#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/15 16:23
# @Author : wangweimin
# @File   : r_picture_label.py
# @Desc   :

from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.picture_operator.picture_label_operator import PictureLabelService, \
    PictureLabelPictureService

PICTURELabelPost = reqparse.RequestParser()
PICTURELabelPost.add_argument('label_name', required=True, type=str, location='form')
PICTURELabelPost.add_argument('catalog_id', required=True, type=int, location='form')
PICTURELabelPost.add_argument('picture_id', required=True, type=int, location='form', action='append')


class PICTURELabel(Resource):

    @error_handler
    def post(self):
        """
        新增图片标签（设置标签）
        ---
        tags:
          - 图片标签
        parameters:
          - name: label_name
            in: formData
            required: true
            type: string
          - name: catalog_id
            in: formData
            required: true
            type: integer
            description: 图片目录id
          - name: picture_id
            in: formData
            type: array
            items:
              type: integer
        responses:
          500:
            description: 添加失败
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
            description: 添加成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                label_id:
                  type: integer
            examples:
              {'code': 0}
        """
        args = PICTURELabelPost.parse_args()
        catalog_id = args['catalog_id']
        label_name = args['label_name']
        pictures_id: list = args['picture_id']
        label_id = PictureLabelService.create(catalog_id=catalog_id, label_name=label_name, pictures_id=pictures_id)
        return jsonify(Response.correct(label_id=label_id))


PICTURELabelOperatorDelete = reqparse.RequestParser()
PICTURELabelOperatorDelete.add_argument('catalog_id', type=int, required=True, location='form')

PICTURELabelOperatorPut = reqparse.RequestParser()
PICTURELabelOperatorPut.add_argument('label_name', type=str, required=True, location='form')
PICTURELabelOperatorPut.add_argument('catalog_id', type=int, required=True, location='form')


class PICTURELabelOperator(Resource):

    @error_handler
    def delete(self, label_id: str):
        """
        删除标签
        ---
        tags:
          - 图片标签
        parameters:
          - name: label_id
            in: path
            required: true
            type: string
          - name: catalog_id
            in: formData
            required: true
            type: integer
            description: 图片目录id
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
              {'message': {'ValueError': 'Error catalog id'}, 'code': 1}
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
        args = PICTURELabelOperatorDelete.parse_args()
        catalog_id = args['catalog_id']
        label_id: int = str2int(label_id)
        PictureLabelService.delete(catalog_id=catalog_id, label_id=label_id)
        return jsonify(Response.correct())

    @error_handler
    def put(self, label_id: str):
        """
        修改标签名称（暂无该功能需求）
        ---
        tags:
          - 图片标签
        parameters:
          - name: label_id
            in: path
            required: true
            type: string
          - name: label_name
            in: formData
            required: true
            type: string
          - name: catalog_id
            in: formData
            required: true
            type: integer
            description: 图片目录id
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
              {'message': {'ValueError': 'Error thumbnail id'}, 'code': 1}
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
        args = PICTURELabelOperatorPut.parse_args()
        catalog_id = args['catalog_id']
        label_name = args['label_name']
        label_id: int = str2int(label_id)
        PictureLabelService.rename(catalog_id=catalog_id, label_id=label_id, label_name=label_name)
        return jsonify(Response.correct())


PICTURELabelPictureDelete = reqparse.RequestParser()
PICTURELabelPictureDelete.add_argument('catalog_id', type=int, required=True, location='form')
PICTURELabelPictureDelete.add_argument('picture_id', required=True, type=int, location='form', action='append')


PICTURELabelPicturePut = reqparse.RequestParser()
PICTURELabelPicturePut.add_argument('catalog_id', type=int, required=True, location='form')
PICTURELabelPicturePut.add_argument('picture_id', required=True, type=int, location='form', action='append')


class PICTURELabelPicture(Resource):

    @error_handler
    def delete(self, label_id: str):
        """
        删除标签下已有图片（不删除图片）
        ---
        tags:
          - 图片标签
        parameters:
          - name: label_id
            in: path
            required: true
            type: string
          - name: catalog_id
            in: formData
            required: true
            type: integer
            description: 图片目录id
          - name: picture_id
            in: formData
            type: array
            items:
              type: integer
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
              {'message': {'ValueError': 'Error catalog id'}, 'code': 1}
          200:
            description: 添加成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0}
        """
        args = PICTURELabelPictureDelete.parse_args()
        catalog_id = args['catalog_id']
        picture_id: list = args['picture_id']
        label_id: int = str2int(label_id)
        PictureLabelPictureService.delete(catalog_id=catalog_id, label_id=label_id, pictures_id=picture_id)
        return jsonify(Response.correct())

    @error_handler
    def put(self, label_id: str):
        """
        给已有图片打已有标签
        ---
        tags:
          - 图片标签
        parameters:
          - name: label_id
            in: path
            required: true
            type: string
          - name: catalog_id
            in: formData
            required: true
            type: integer
            description: 图片目录id
          - name: picture_id
            in: formData
            type: array
            items:
              type: integer
        responses:
          500:
            description: 添加失败
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
            description: 添加成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0}
        """
        args = PICTURELabelPicturePut.parse_args()
        catalog_id = args['catalog_id']
        picture_id: list = args['picture_id']
        label_id: int = str2int(label_id)
        PictureLabelPictureService.add(catalog_id=catalog_id, label_id=label_id, pictures_id=picture_id)
        return jsonify(Response.correct())
