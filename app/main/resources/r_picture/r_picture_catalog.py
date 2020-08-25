#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/15 10:50
# @Author : wangweimin
# @File   : r_picture_catalog.py
# @Desc   :


from flask import jsonify
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.resources_config import PermitAscriptionType
from app.main.resources.r_base.request_param_judgement import one_and_the_only
from app.main.resources.r_base.request_data_transform import str2int
from app.main.resources.r_base.resources_response import Response
from app.main.services.operator.picture_operator.application_picture_catalog_operator import AppPictureCatalogService
from app.main.services.operator.picture_operator.project_picture_catalog_operator import ProPictureCatalogService
from app.main.services.operator.picture_operator.picture_catalog_ioperator import PictureCatalogLabelService, \
    PictureCatalogService
from app.models import User

PICTURECatalogPost = reqparse.RequestParser()
PICTURECatalogPost.add_argument('project_id', type=str, location='form')
PICTURECatalogPost.add_argument('application_id', type=str, location='form')
PICTURECatalogPost.add_argument('catalog_name', required=True, type=str, location='form')
PICTURECatalogPost.add_argument('label_name', type=str, location='form')
PICTURECatalogPost.add_argument('pictures', required=True, type=FileStorage, location='files', action='append')


class PICTURECatalog(Resource):

    @error_handler
    def post(self):
        """
        新建图片目录并上传文件
        ---
        tags:
          - 图片目录
        parameters:
          - name: project_id
            in: formData
            type: integer
            description: 若为应用数据，不传递该参数
          - name: application_id
            in: formData
            type: integer
            description: 若为工程原始数据，不传递该参数
          - name: catalog_name
            in: formData
            type: string
            required: true
            description: 图片目录名称（即工程下的数据名称）
          - name: label_name
            in: formData
            type: string
            description: 图片标签
          - name: pictures
            in: formData
            type: file
            required: true
            description: 文件流，此处只提供上传一个文件的测试功能，实际可上传多个！
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
              {'message': {'ValueError': 'Error project id'}, 'code': 1}
          200:
            description: 上传图片成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                picture_catalog_id:
                  type: integer
            examples:
              {'code': 0}
        """
        args = PICTURECatalogPost.parse_args()
        project_id = args['project_id'] or None
        application_id = args['application_id'] or None
        one_and_the_only(project_id, application_id)
        catalog_name = args['catalog_name']
        label_name = args['label_name']
        pictures = args['pictures']
        creator_id: int = User.query.first().id
        if project_id:
            picture_catalog_id = ProPictureCatalogService.create(project_id=project_id, label_name=label_name,
                                                                 catalog_name=catalog_name,
                                                                 pictures=pictures, creator_id=creator_id)
        else:
            picture_catalog_id = AppPictureCatalogService.create(application_id=application_id,
                                                                 catalog_name=catalog_name,
                                                                 pictures=pictures, creator_id=creator_id)
        return jsonify(Response.correct(picture_catalog_id=picture_catalog_id))


PICTURECatalogOperatorPost = reqparse.RequestParser()
PICTURECatalogOperatorPost.add_argument('label_name', type=str, location='form')
PICTURECatalogOperatorPost.add_argument('pictures', required=True, type=FileStorage, location='files', action='append')

PICTURECatalogOperatorDelete = reqparse.RequestParser()
PICTURECatalogOperatorDelete.add_argument('is_forced', type=int, location='form', choices=(0, 1))
PICTURECatalogOperatorDelete.add_argument('ascription', type=str, location='form', choices=PermitAscriptionType)

PICTURECatalogOperatorPut = reqparse.RequestParser()
PICTURECatalogOperatorPut.add_argument('catalog_name', required=True, type=str, location='form')
PICTURECatalogOperatorPut.add_argument('ascription', type=str, location='form', choices=PermitAscriptionType)


class PICTURECatalogOperator(Resource):

    @error_handler
    def post(self, catalog_id: str):
        """
        导入新图片到已有图片目录中
        ---
        tags:
          - 图片目录
        parameters:
          - name: catalog_id
            in: path
            required: true
            type: integer
          - name: label_name
            in: formData
            type: string
            description: 图片标签
          - name: pictures
            in: formData
            type: file
            required: true
            description: 文件流，此处只提供上传一个文件的测试功能，实际可上传多个！
        responses:
          500:
            description: 上传失败
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
            description: 上传成功
            schema:
              properties:
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0}
        """
        args = PICTURECatalogOperatorPost.parse_args()
        label_name = args['label_name']
        pictures = args['pictures']

        creator_id: int = User.query.first().id
        catalog_id = str2int(catalog_id)
        PictureCatalogService.add_newly(catalog_id=catalog_id, pictures=pictures, label_name=label_name,
                                        creator_id=creator_id)
        return jsonify(Response.correct())

    @error_handler
    def delete(self, catalog_id: str):
        """
        删除图片目录
        ---
        tags:
          - 图片目录
        parameters:
          - name: catalog_id
            in: path
            required: true
            type: integer
          - name: is_forced
            in: formData
            type: integer
            default: 0
            description: 是否在被模型使用的情况下强制删除,0(默认)表示否,1表示强制删除（只适用于工程下数据）
          - name: ascription
            in: formData
            type: string
            default: project
            description: 该数据若归属于工程，传递project，若归属于应用，传递application，不传值默认为project
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
              {'message': {'ValueError': 'Error picture id'}, 'code': 1}
          200:
            description: 删除状态，若code为0，删除成功，若为2，则需要强制删除
            schema:
              properties:
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0}
        """
        args = PICTURECatalogOperatorDelete.parse_args()
        is_forced = args['is_forced'] or 0
        ascription = args['ascription'] or 'project'
        catalog_id = str2int(catalog_id)
        if 'project' == ascription:
            status = ProPictureCatalogService.delete(catalog_id=catalog_id, is_forced=is_forced)
        else:
            status = AppPictureCatalogService.delete(catalog_id=catalog_id)
        if status:
            return jsonify(Response.correct())
        else:
            return jsonify(Response.force())

    @error_handler
    def get(self, catalog_id: str):
        """
        获取目录下已有标签图片数量及无标签图片数量
        ---
        tags:
          - 图片目录
        parameters:
          - name: catalog_id
            in: path
            required: true
            type: integer
            description: 图片目录（工程数据）的id
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
              {'message': {'ValueError': 'Error catalog id'}, 'code': 1}
          200:
            description: 获取成功
            schema:
              properties:
                non_label_count:
                  type: integer
                label:
                  type: array
                  items:
                    - name: label_name
                      type: string
                    - name: label_id
                      type: integer
                    - name: pictures_count
                      type: integer
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'non_label_count': '10', 'label': [{'label_name': 'normal', 'label_id': 2, 'pictures_count': 20}]}
        """
        creator_id: int = User.query.first().id
        catalog_id = str2int(catalog_id)
        result: dict = PictureCatalogLabelService.info(catalog_id=catalog_id, creator_id=creator_id)
        return jsonify(Response.correct(**result))

    @error_handler
    def put(self, catalog_id: str):
        """
        修改图片目录名称
        ---
        tags:
          - 图片目录
        parameters:
          - name: catalog_id
            in: path
            type: integer
            required: true
            description: 图片目录id
          - name: catalog_name
            in: formData
            type: string
            required: true
          - name: ascription
            in: formData
            type: string
            default: project
            description: 该数据若归属于工程，传递project，若归属于应用，传递application，不传值默认为project
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
              {'message': {'ValueError': 'Error catalog id'}, 'code': 1}
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
        args = PICTURECatalogOperatorPut.parse_args()
        catalog_name = args['catalog_name']
        ascription = args['ascription'] or 'project'
        catalog_id = str2int(catalog_id)
        if 'project' == ascription:
            ProPictureCatalogService.rename(catalog_id=catalog_id, catalog_name=catalog_name)
        else:
            AppPictureCatalogService.rename(catalog_id=catalog_id, catalog_name=catalog_name)
        return jsonify(Response.correct())


class PICTURECatalogLabel(Resource):

    @error_handler
    def get(self, catalog_id: str):
        """
        获取图片目录下已有标签
        ---
        tags:
          - 图片目录
        parameters:
          - name: catalog_id
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
              {'message': {'ValueError': 'Error catalog id'}, 'code': 1}
          200:
            description: 获取成功
            schema:
              properties:
                catalog_name:
                  type: string
                data:
                  type: array
                  items:
                    - name: label_name
                      type: string
                    - name: label_id
                      type: integer
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'catalog_name': 'pic', 'data': [{'label_name': 'x', 'label_id': 1}, {'label_name': 'y', 'label_id': 2}]}
        """
        catalog_id = str2int(catalog_id)
        result = PictureCatalogService.labels(catalog_id=catalog_id)
        return jsonify(Response.correct(**result))


PICTURECatalogPictureGet = reqparse.RequestParser()
PICTURECatalogPictureGet.add_argument('label_id', required=True, type=int, location='args')
PICTURECatalogPictureGet.add_argument('page', required=True, type=int, location='args')
PICTURECatalogPictureGet.add_argument('limit', required=True, type=int, location='args')


class PICTURECatalogPicture(Resource):

    @error_handler
    def get(self, catalog_id: str):
        """
        获取目录下特定标签图片信息
        ---
        tags:
          - 图片目录
        parameters:
          - name: catalog_id
            in: path
            required: true
            type: integer
          - name: label_id
            in: query
            required: true
            type: integer
            description: 0表示所有图片，-1表示无标签图片，默认为0
          - name: page
            in: query
            type: integer
            required: true
            description: 页码
          - name: limit
            in: query
            type: integer
            required: true
            default: 20
            description: 每页图片量
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
              {'message': {'ValueError': 'Error catalog id'}, 'code': 1}
          200:
            description: 获取成功
            schema:
              properties:
                data:
                  type: array
                  items:
                    - name: picture_id
                      type: integer
                    - name: thumbnail_url
                      type: string
                    - name: picture_name
                      type: string
                    - name: original_url
                      type: string
                    - name: size
                      type: integer
                catalog_name:
                  type: string
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'data': [{'picture_id': 1, 'thumbnail_url': '/thumbnail/a.png', 'picture_name': '2019a.jpg', 'original_url': '/original/a.png', 'size': '375134'}]}
        """
        args = PICTURECatalogPictureGet.parse_args()
        label_id = args['label_id'] or 0
        page = args['page']
        page = page if page > 0 else 1
        limit = args['limit']
        catalog_id = str2int(catalog_id)
        result = PictureCatalogService.pictures_info(catalog_id=catalog_id, limit=limit, page=page,
                                                     label_id=label_id)
        return jsonify(Response.correct(**result))


class PICTURECatalogPictureName(Resource):

    @error_handler
    def get(self, catalog_id: str):
        """
        获取目录名称及其下已有图片名称
        ---
        tags:
          - 图片目录
        parameters:
          - name: catalog_id
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
              {'message': {'ValueError': 'Error catalog id'}, 'code': 1}
          200:
            description: 获取成功
            schema:
              properties:
                data:
                  type: array
                  items:
                    type: string
                code:
                  type: integer
                  default: 0
            examples:
              {'code': 0, 'data': ['asd.jpg', 'sd.png']}
        """
        catalog_id = str2int(catalog_id)
        result: list = PictureCatalogService.picture_names(catalog_id=catalog_id)
        return jsonify(Response.correct(data=result))
