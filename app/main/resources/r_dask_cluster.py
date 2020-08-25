#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/17 14:21
# @Author : wangweimin
# @File   : r_dask_cluster.py
# @Desc   :

from flask import jsonify
from flask_restful import Resource, reqparse

from app.main.services.message.dask_cluster import dask_cluster_address
from app.models import DaskCluster


DaskClusterGet = reqparse.RequestParser()
DaskClusterGet.add_argument('cluster_id', type=int, location='args')


class DASKCluster(Resource):

    def get(self):
        """
        获取dask集群信息
        ---
        tags:
          - dask
        parameters:
          - name: cluster_id
            in: query
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
            examples:
              {'message': {'ValueError': 'Error cluster id'}}
          200:
            description: 数据
            schema:
              properties:
                address:
                  type: string
            examples:
              {'address': '127.0.0.1:8786'}
        """
        args = DaskClusterGet.parse_args()
        cluster_id = args['cluster_id'] or DaskCluster.query.first().id
        try:
            address = dask_cluster_address(cluster_id=cluster_id)
            return jsonify({'address': address})
        except Exception as e:
            return jsonify({'message': {e.__class__.__name__: str(e)}})
