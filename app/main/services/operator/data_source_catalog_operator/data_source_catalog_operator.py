#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/19 16:49
# @Author : wangweimin
# @File   : data_source_catalog_operator.py
# @Desc   :

from app import db
from app.models import DataSourceCatalog, DataSourceDataLink


def ds_catalog_create_service(catalog_pid: int, catalog_name: str, user_id: int):
    data_catalog: DataSourceCatalog = DataSourceCatalog.query.get(catalog_pid)
    if data_catalog is None:
        raise ValueError('Error catalog pid')
    if not DataSourceCatalog.query.filter(DataSourceCatalog.name == catalog_name).first():
        data_catalog: DataSourceCatalog = DataSourceCatalog(name=catalog_name, pid=catalog_pid, creator_id=user_id)
        db.session.add(data_catalog)
        db.session.commit()
    else:
        raise ValueError('Repeated catalog name!')
    return


def ds_catalog_delete_service(catalog_id: int):
    data_catalog: DataSourceCatalog = DataSourceCatalog.query.get(catalog_id)
    if not data_catalog:
        raise ValueError('Error catalog id')
    # 判断该目录下是否有数据或目录，有才可以删除，没有则删除失败
    if DataSourceCatalog.query.filter(
            DataSourceCatalog.pid == catalog_id).first() or DataSourceDataLink.query.filter(
            DataSourceDataLink.catalog_id == catalog_id).first():
        raise IOError('Exist child catalog or data in this catalog')
    else:
        db.session.delete(data_catalog)
        db.session.commit()
    return


def ds_catalog_modify_service(catalog_id: int, catalog_name: str):
    # 不允许重名
    if not DataSourceCatalog.query.filter(DataSourceCatalog.name == catalog_name).first():
        data_catalog: DataSourceCatalog = DataSourceCatalog.query.get(catalog_id)
        if data_catalog is None:
            raise ValueError('Error catalog id')
        else:
            data_catalog.name = catalog_name
            db.session.commit()
    else:
        raise ValueError('Repeated catalog name!')
    return
