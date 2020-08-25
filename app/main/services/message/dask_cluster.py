#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/17 14:32
# @Author : wangweimin
# @File   : m_dask_cluster.py
# @Desc   :

from app.models import DaskCluster


def dask_cluster_address(cluster_id: int) -> str:
    dask_cluster: DaskCluster = DaskCluster.query.get(cluster_id)
    if dask_cluster is None:
        raise ValueError('Error dask cluster id')
    return ':'.join([dask_cluster.ip, dask_cluster.port])
