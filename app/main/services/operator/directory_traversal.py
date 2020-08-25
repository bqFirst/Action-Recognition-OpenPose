#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/7 17:10
# @Author : wangweimin
# @File   : directory_traversal.py
# @Desc   :

from app.models import DataSourceCatalog


def dir_traversal_service(type_, catalog_id: int) -> list:
    """

    :param type_: 需遍历的目录类型
        type_='data_source' 则遍历特定的数据源目录
        type_='project' 则遍历特定的工程目录
        type_='application' 则遍历特定的应用目录
    :param catalog_id:
    :return:
    """
    # Todo
    # 暂不返回子目录
    if 'data_source' == type_:
        catalog = DataSourceCatalog.query.get(catalog_id)
        data_links = catalog.data_links.all()
    else:
        data_links = []

    data_list = []
    for data_link in data_links:
        data_link_name = data_link.name
        data_list.append(data_link_name)
    return data_list
