#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/3/4 16:33
# @Author : wangweimin
# @File   : r_user.py
# @Desc   :


from flask import g
from flask_restful import Resource, reqparse

from app.main.resources.r_base.resources_response import Response

from app.main.resources.r_base.r_aop.error_handler import error_handler
from app.main.resources.r_base.r_aop.ramadi_authentication import auth, basic_auth
from app.main.services.operator.user_operator.user_operator import UserService

USERPost = reqparse.RequestParser()
USERPost.add_argument('username', required=True, type=str, location='form')
USERPost.add_argument('password', required=True, type=str, location='form')

USERPut = reqparse.RequestParser()
USERPut.add_argument('username', required=True, type=str, location='form')
USERPut.add_argument('telephone', required=True, type=str, location='form')


class USER(Resource):

    @error_handler
    def post(self):
        """
        用户创建
        ---
        tags:
          - 用户
        parameters:
          - name: username
            in: formData
            type: string
            required: true
            description: 用户名
          - name: password
            in: formData
            type: string
            required: true
            description: 密码
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
              {'message': {'ValueError': 'Username has existed'}, 'code': 1}
          200:
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                data:
                  items:
                    - name: token
                      type: string
            examples:
              {'code': 0, 'data': {'token': 'asfacbsbdfcvmwehjsdbhcbjk'}}
        """
        args = USERPost.parse_args()
        username = args['username']
        password = args['password']
        token = UserService.create(username=username, password=password)
        return Response.correct(token=token)

    @auth.login_required
    @error_handler
    def put(self):
        """
        用户信息修改
        ---
        tags:
          - 用户
        parameters:
          - name: username
            in: formData
            type: string
            required: true
            description: 用户名
          - name: telephone
            in: formData
            default: '14111111111'
            type: string
            required: true
            description: 密码
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
              {'message': {'ValueError': 'Username has existed'}, 'code': 1}
          200:
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                data:
                  items:
                    - name: token
                      type: string
            examples:
              {'code': 0, 'data': {'token': 'asfacbsbdfcvmwehjsdbhcbjk'}}
        """
        args = USERPut.parse_args()
        username = args['username']
        telephone = args['telephone']
        UserService.modify(username=username, telephone=telephone, user=g.user)
        return Response.correct()


class USERToken(Resource):
    decorators = [basic_auth.login_required, error_handler]

    def get(self):
        """
        用户创建
        ---
        tags:
          - 用户
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
              {'message': {'ValueError': 'Username has existed'}, 'code': 1}
          200:
            schema:
              properties:
                code:
                  type: integer
                  default: 0
                data:
                  items:
                    - name: token
                      type: string
            examples:
              {'code': 0, 'data': {'token': 'asfacbsbdfcvmwehjsdbhcbjk'}}
        """
        token = UserService.get_token(user=g.user)
        return Response.correct(token=token)
