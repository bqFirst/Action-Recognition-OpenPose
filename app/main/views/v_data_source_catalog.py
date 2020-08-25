#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/23 9:02
# @Author : wangweimin
# @File   : v_data_source_catalog.py
# @Desc   :


from flask import request, jsonify

from app import db
from app.main.main import main
from app.main.services.operator.catalog_operator import data_source_tree
from app.models import DataSourceCatalog, DataSourceDataLink


@main.route('/ds/catalog/create', methods=['POST'])
def ds_catalog_create():
    res = dict(code=-1, msg=None)
    # 若是最根级目录，pid为0
    catalog_pid = int(request.form['catalog_pid'])
    catalog_name = request.form['catalog_name']
    user_id = int(request.form['user_id'])  # 默认使用1
    # 不允许重名
    if not DataSourceCatalog.query.filter(DataSourceCatalog.name == catalog_name).first():
        data_catalog: DataSourceCatalog = DataSourceCatalog(name=catalog_name, pid=catalog_pid, creator_id=user_id)
        db.session.add(data_catalog)
        db.session.commit()
        res.update(code=0, msg='success')
    else:
        res.update(msg='Repeated catalog name!')
    return jsonify(res)


@main.route('/ds/catalog/delete', methods=['POST'])
def ds_catalog_delete():
    res = dict(code=-1, msg=None)
    catalog_id = int(request.form['catalog_id'])
    data_catalog: DataSourceCatalog = DataSourceCatalog.query.get(catalog_id)
    if not data_catalog:
        res.update(msg='Error catalog id')
    else:
        # 判断该目录下是否有数据或目录，有才可以删除，没有则删除失败
        if DataSourceCatalog.query.filter(
                DataSourceCatalog.pid == catalog_id).first() or DataSourceDataLink.query.filter(
                DataSourceDataLink.catalog_id == catalog_id).first():
            res.update(msg='Exist child catalog or data in this catalog')
        else:
            db.session.delete(data_catalog)
            db.session.commit()
            res.update(code=0, msg='success')
    return jsonify(res)


@main.route('/ds/catalog/modify', methods=['POST'])
def ds_catalog_modify():
    res = dict(code=-1, msg=None)
    catalog_id = int(request.form['catalog_id'])
    catalog_name = request.form['catalog_name']
    # 不允许重名
    if not DataSourceCatalog.query.filter(DataSourceCatalog.name == catalog_name).first():
        data_catalog: DataSourceCatalog = DataSourceCatalog.query.get(catalog_id)
        if data_catalog is None:
            res.update(msg='Error catalog id')
        else:
            data_catalog.name = catalog_name
            db.session.commit()
            res.update(code=0, msg='success')
    else:
        res.update(msg='Repeated catalog name!')
    return jsonify(res)


@main.route('/ds/catalog/get/menu', methods=['GET'])
def ds_catalog_get_menu():
    tree = data_source_tree(catalog_id=0)
    return jsonify({'data': tree})
