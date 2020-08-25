#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/17 10:49
# @Author : wangweimin
# @File   : m_dask_cluster.py
# @Desc   :

from app import db


class DaskCluster(db.Model):
    __tablename__ = 't_dask_clusters'

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), nullable=False)
    port = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        return '<dask cluster: {}:{}>'.format(self.ip, self. port)
