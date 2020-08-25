#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/23 17:51
# @Author : wangweimin
# @File   : data_source_operator.py
# @Desc   :

from app import db
from app.models import DataSourceCatalog, DataSourceDataLink


def catalog_data_link_info(catalog_id: int) -> list:
    result = []
    if 0 == catalog_id:
        data_links: list = DataSourceDataLink.query.all()
    else:
        data_source_catalog: DataSourceCatalog = DataSourceCatalog.query.get(catalog_id)
        if data_source_catalog is None:
            raise ValueError('Error catalog id')
        data_links = data_source_catalog.data_links.all()
    for data_link in data_links:
        data_msg = dict()
        data_msg['creator'] = data_link.creator.name
        data_msg['data_link_id'] = data_link.id
        data_msg['create_time'] = data_link.create_time
        data_msg['data_name'] = data_link.name
        data_msg['data_link_type'] = data_link.data_type.data_type
        # data_type_id = data_link.data_type_id
        # data_name: str = data_link.name
        # if 1 == data_type_id:
        #     data_msg['name'], data_msg['data_type'] = data_name.rsplit('.', 1)
        # else:
        #     data_msg['name'], data_msg['data_type'] = data_name, 'database'
        result.append(data_msg)
    return result


def ds_data_link_info() -> list:
    result = []
    query = db.session().query(DataSourceDataLink, DataSourceCatalog)
    datas = query.join(DataSourceDataLink, DataSourceDataLink.catalog_id == DataSourceCatalog.id).all()
    for data in datas:
        catalog: DataSourceCatalog = data.DataSourceCatalog
        data_link: DataSourceDataLink = data.DataSourceDataLink
        data_msg = dict()
        data_type_id = data_link.data_type_id
        data_msg['creator'] = data_link.creator.name
        data_msg['data_id'] = data_link.id
        data_msg['create_time'] = data_link.create_time
        data_name: str = data_link.name
        if 1 == data_type_id:
            data_msg['name'], data_msg['data_type'] = data_name.rsplit('.', 1)
        else:
            data_msg['name'], data_msg['data_type'] = data_name, 'database'
        data_msg['catalog'] = catalog.name
        result.append(data_msg)
    return result
