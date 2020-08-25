#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/2 11:14
# @Author : wangweimin
# @File   : test.py
# @Desc   :

from flask_restful import Resource
from flask import jsonify


class HelloWorld(Resource):

    def get(self):
        """
        This is the language awesomeness API
        Call this api passing a language name and get back its features
        ---
        tags:
          - Awesomeness Language API
        parameters:
          - name: data
            in: query
            type: dict
            required: true
            description: dataframe
        responses:
          500:
            description: Error The language is not awesome!
          200:
            description: A language with its awesomeness
            schema:
              id: awesome
              properties:
                data:
                  type: string
                  description: The language name
                  default: 'a'
            examples:
              a: 12
        """
        return jsonify({'a': 12})

    def put(self):
        return jsonify({'b': 11})

    def post(self):
        return jsonify({'c': 10})


temp = """
        描述
        ---
        tags:
          - Awesomeness Language API
        parameters:
          - name: data
            in: query
            type: dict
            required: true
            description: dataframe
        responses:
          500:
            description: 获取失败
            schema:
              properties:
                code:
                  type: integer
                  default: -1
                msg:
                  type: string
                  description: 失败原因
            examples:
              {'code': -1, 'msg': 'Error data link id'}
          200:
            description: A language with its awesomeness
            schema:
              properties:
                data:
                  type: string
                  description: The language name
                  default: 'a'
            examples:
              code: 0
        """
