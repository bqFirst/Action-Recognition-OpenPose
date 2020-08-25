#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/18 9:55
# @Author : wangweimin
# @File   : dask_client.py
# @Desc   :

from dask.distributed import Client

from app.main.modeling.dask.myerror import CreateDaskClusterError
from app.models import DaskCluster


class DaskClient(object):
    def __init__(self, pattern: str='local'):
        """
        create a distributed client, it will start up a local scheduler or on a cluster
        :param pattern: the type of the distributed client you want to create, local or cluster
        """
        self.__client: Client = None
        self.__init(pattern=pattern)

    def __init(self, pattern: str):
        if pattern not in ['local', 'cluster']:
            raise ValueError('parameter `pattern` only support \'local\' or \'cluster\'')
        try:
            if 'local' == pattern:
                self.__client = Client()
            else:
                dask_cluster: DaskCluster = DaskCluster.query.first()
                address = ':'.join([dask_cluster.ip, dask_cluster.port])
                self.__client = Client(address)
        except Exception as e:
            raise CreateDaskClusterError(str(e))

    def __del__(self):
        self.close()

    def reset(self, pattern: str='local'):
        """
        reset your distributed client
        :param pattern: the type of the distributed client you want to create, local or cluster
        :return:
        """
        self.close()
        self.__init(pattern=pattern)

    def close(self):
        """
        close your distributed client
        :return:
        """
        if isinstance(self.__client, Client):
            self.__client.close()
