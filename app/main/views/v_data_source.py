#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/7/30 10:56
# @Author : wangwei
# @File   : v_data_source.py
# @Desc   :

import datetime
import os

import openpyxl
import pandas as pd
from flask import request, jsonify, render_template, url_for, send_from_directory

from app import db
from app.main.main import main
from app.main.services.operator.base_common.file_operator import file_write_service
from app.main.services.operator.data_source_operator import catalog_data_link_info, ds_data_link_info
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.models import DataSourceDataLink, User, DataSourceCatalog
from conf.data_path import DataDirectoryPath


# 文件上传存放的文件夹, 值为非绝对路径时，相对于项目根目录


# 文件名合法性验证
def allowed_execl_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1] in ['xls', 'xlsx', 'csv']


@main.route("/ds")
def index_view():
    """主页视图"""
    return render_template("data-source.html")


@main.route('/ds/showimg/<filename>')
def showimg_view(filename):
    print("路径：", FILE_FOLDER)
    return send_from_directory(FILE_FOLDER, filename)


@main.route('/ds/upload/excel', methods=['POST', 'OPTIONS'])
def upload_view():
    res = dict(code=-1, msg=None, file_name="", file_id="", catalog_id="", path="")
    f = request.files.get('file')
    # Todo
    # 获取datasource路径
    catalog_id = int(request.form['catalog_id'])
    user_id = User.query.first().id
    if f and allowed_execl_file(f.filename):
        filename = f.filename
        try:
            alias = file_write_service(f=f, address='data_source')
            data_link = DataSourceDataLink(name=filename, alias=alias, data_type_id=1, creator_id=user_id,
                                           catalog_id=catalog_id)
            db.session.add(data_link)
            db.session.commit()
            file_url = url_for('main.showimg_view', filename=filename, _external=True)
            # res.update(code=0, data=dict(src=file_url))
            path = DataDirectoryPath.get_data_source_path() + '\\' + alias

            res.update(code=0, file_name=data_link.name, file_id=data_link.id,
                       catalog_id=data_link.catalog_id, path=path)
        except Exception as e:
            res.update(msg=str(e))
    else:
        res.update(msg="Unsuccessfully obtained file or format is not allowed")
    return jsonify(res)


# 表单提交url
# @main.route("/ds/filePreview", methods=['POST', 'OPTIONS'])
# def file_preview():
@main.route('/ds/preview/data', methods=['POST', 'OPTIONS'])
def preview_data():
    # msg = {"code": 0, "url": "/DataI/FileDataLink/filePreview"}
    file_name = request.form['fileName']
    file_type = request.form['fileType']
    file_path = request.form['filePath']
    file_id = request.form['fileId']
    catalog_id = request.form['catalogId']

    time = datetime.datetime.now()

    catalogs = []
    catas = DataSourceCatalog.query.all()
    for catalog in catas:
        catalogs.append({"name": catalog.name, "catalog_id": catalog.id})

    data_link = {"name": file_name, "data_id": file_id, "data_type": file_type, "create_time": time, "creator": "wangw"}

    return render_template("file-conn.html", data_link=data_link, catalogs=catalogs, sheets="")


@main.route('/ds/get/data_list', methods=['GET'])
def ds_list():
    result = ds_data_link_info()
    res = {'name': "所有目录", 'count': (len(result)), 'data': result}
    return render_template("data-links-index.html", **res)
    # return jsonify(res)


# @main.route("/ds/datalink/index", methods=['GET'])
# def query_data_links():
@main.route('/ds/catalog/get/data/info', methods=['GET'])
def query_data_info():
    catalog_id = request.values.get('catalog_id') or '1'
    result = catalog_data_link_info(catalog_id=int(catalog_id))

    res = {'name': "所有目录", 'count': (len(result)), 'data': result}

    return render_template("data-links-index.html", **res)
    # return jsonify({'data': res})


@main.route('/ds/catalog/get/group/<catalog_id>', methods=['GET'])
def ds_catalog_get_group(catalog_id):
    catalog_id = catalog_id  # request.values.get('catalog_id') or '1'

    catalog = DataSourceCatalog.query.get(int(catalog_id))
    catalog_id = int(catalog_id)
    result = catalog_data_link_info(catalog_id=catalog_id)
    res = {'name': catalog.name, 'count': (len(result)), 'data': result}
    return render_template("data-links-index.html", **res)
    # return jsonify(res)


# @main.route("/ds/rename/<data_id>",methods=["POST"])
# def rename(data_id):
@main.route('/ds/rename/data/<data_link_id>', methods=['POST'])
def rename_data(data_link_id):
    # data_link_id = int(data_link_id)
    print(data_link_id)
    res = {"code": -1}  # "msg":["INUSE","ERROR","NOTFOUND"]
    data_link: DataSourceDataLink = DataSourceDataLink.query.get(data_link_id)
    if not data_link:
        res['msg'] = 'Error data link id'
    else:
        new_name: str = request.values['name']
        old_name: str = data_link.name
        data_type_id: int = data_link.data_type_id
        if 1 == data_type_id:
            suffix: str = old_name.rsplit('.', 1)[-1]
            data_link.name = '.'.join([new_name, suffix])
        else:
            data_link.name = new_name
        db.session.commit()
        res.update(code=0, msg='SUCCESS')
    return jsonify(res)


# @main.route("/ds/delete/<data_id>", methods=['POST'])
# def delete(data_id):
@main.route("/ds/delete/data/<data_link_id>", methods=['POST'])
def delete_data(data_link_id):
    data_link_id = int(data_link_id)
    res = {"code": -1, }  # "msg":["INUSE","ERROR","NOTFOUND"]
    data_link: DataSourceDataLink = DataSourceDataLink.query.get(data_link_id)
    if not data_link:
        res['msg'] = 'Error data link id'
    else:
        db.session.delete(data_link)
        db.session.commit()
        res.update(code=0, msg='SUCCESS')
    return jsonify(res)


# @main.route("/ds/datalink/update", methods=['POST'])
# def datalink_update():
@main.route("/ds/subdirectory/data", methods=['POST'])
def subdirectory_data():
    """更改文件所属目录"""
    data_link_id = int(request.values['data_link_id'])
    print("167: ", data_link_id, type(data_link_id))
    catalog_id = request.values['catalog_id']
    res = {'code': -1}
    data_link: DataSourceDataLink = DataSourceDataLink.query.get(data_link_id)
    if not data_link:
        res['msg'] = 'Error data link id'
    else:
        data_link.catalog_id = catalog_id
        db.session.commit()
        res.update(code=0, msg='success')
    return jsonify(res)


# @main.route("/FileDataLink/update", methods=['POST'])
# def file_data_link_update():
@main.route('/ds/modify/data', methods=['POST'])
def modify_data():
    # 根据文件id，更新文件文件名，目录
    data_link_id = request.values['data_link_id']
    print("185:", data_link_id, type(data_link_id))

    new_name = request.values['data_link_name']
    catalog_id = request.values['catalog_id']
    res = {'code': -1, "status": ""}

    data_link: DataSourceDataLink = DataSourceDataLink.query.get(data_link_id)
    if not data_link:
        res['msg'] = 'Error data link id'
    else:
        old_name: str = data_link.name
        data_type_id: int = data_link.data_type_id
        if 1 == data_type_id:
            suffix: str = old_name.rsplit('.', 1)[-1]
            data_link.name = '.'.join([new_name, suffix])
        else:
            data_link.name = new_name
        data_link.catalog_id = catalog_id
        db.session.commit()
        res.update(code=0, msg='success', status="SUCCESS")
    return jsonify(res)


# @main.route("/demo/table/user/<data_id>/<sheet_name>")
# def get_table_data(data_id, sheet_name):
@main.route('/ds/get/file/paging/data/<data_id>/<sheet_name>')
def get_paging_data(data_id, sheet_name):
    """
    查询并返回sheet_name下的数据
    :param data_id:
    :param sheet_name:
    :return:
    """
    d_link = DataSourceDataLink.query.get(data_id)

    type = d_link.name.split('.')[-1]

    if type.lower() in ['xlsx', 'xls', 'excel']:

        try:
            df = DataFileOperator(address='data_source').get(filename=d_link.alias, sheet_name=sheet_name)
            df = df.fillna(value="")
        except Exception as e:
            return jsonify({'code': -1})
        res = dict()
        res['code'] = 0
        res['count'] = df.shape[0]
        res['data'] = df.to_dict(orient='record')
        return jsonify(res)
    elif type.lower() in ['csv']:
        try:
            df = DataFileOperator(address='data_source').get(filename=d_link.alias)
            df = df.fillna("")
            # 数据太大，导致页面加载不过来，在此设置页面显示数据为100条
            df = df[:100]
        except Exception as e:
            return jsonify({'code': -1})
        res = dict()
        res['code'] = 0
        res['count'] = df.shape[0]
        res['data'] = df.to_dict(orient='record')
        return jsonify(res)


# @main.route("/dataEdit/ViewMain/<data_id>/<sheet_name>", methods=['GET'])
# def view_main(data_id, sheet_name):
@main.route('/ds/get/file/paging/info/<data_id>/<sheet_name>', methods=['GET'])
def get_paging_info(data_id, sheet_name):
    """
    解析并返回文件表头,sheet_name 列表
    :param data_id: 文件id
    :param sheet_name:
    :return:
    """

    sheet_id = ""
    # 通过data_id, sheet_id 解析excel表头
    d_link = DataSourceDataLink.query.get(data_id)
    type = d_link.name.split('.')[-1]

    if type.lower() in ['xlsx', 'xls', 'excel']:

        df = DataFileOperator(address='data_source').get(filename=d_link.alias, sheet_name=sheet_name)
        df = df.fillna(value="")
        cols = df.columns[1:]
        table = {"sheet_name": sheet_name, "data_id": data_id, "sheet_id": sheet_id}
        return render_template('file-conn-table-edit.html', cols=cols, sheet=table)
    elif type.lower() in ['csv']:
        df = DataFileOperator(address='data_source').get(filename=d_link.alias)
        df = df.fillna(value="")
        cols = df.columns
        table = {"sheet_name": sheet_name, "data_id": data_id, "sheet_id": sheet_id}
        return render_template('file-conn-table-edit.html', cols=cols, sheet=table)


# @main.route("/FileDataLink/deleteTable")
# def delete_table():
@main.route('/ds/delete/file/paging/data', methods=['POST'])
def delete_paging():
    """
    删除sheet_name下的数据
    :return:
    """
    res = dict(code=-1)
    data_id = request.form['data_id']
    sheet_name = request.form['sheet_name']

    data_link: DataSourceDataLink = DataSourceDataLink.query.get(int(data_id))
    if not data_link:
        res.update(msg='Error')
    else:
        file = os.path.join(DataDirectoryPath.get_data_source_path(), data_link.alias)
        reader = pd.ExcelFile(file)
        sheet_names: list = reader.sheet_names
        if sheet_name not in sheet_names:
            res.update(code=0, msg='success')
        elif 1 == len(sheet_names):
            alias = data_link.alias
            # Todo
            # 若文件被引用，无法删除
            DataFileOperator(address='data_source').delete(file_name=alias)
            db.session.delete(data_link)
            db.session.commit()
        else:
            try:
                wb = openpyxl.load_workbook(file)
                ws = wb[sheet_name]
                wb.remove(ws)
                wb.save(file)
            except Exception as e:
                res.update(msg=str(e))
            else:
                res.update(msg='success')
    return jsonify(res)


@main.route("/ds/data_list/main/<catalog_id>", methods=['GET'])
def data_link_main(catalog_id):
    result = catalog_data_link_info(catalog_id=catalog_id)
    data_links = {'name': "所有目录", 'count': (len(result)), 'data': result}
    # return render_template("data-source.html", **data_links)
    return jsonify(data_links)


# @main.route("/ds/edit/<data_id>", methods=['GET'])
# def edit(data_id):
@main.route("/ds/edit/data/<data_link_id>", methods=['GET'])
def edit_data(data_link_id):
    # data_link_id = int(data_link_id)
    # 根据data_id 获取文件属性 目录,如下
    data_link = DataSourceDataLink.query.get(data_link_id)
    # 解析sheet name
    path = os.path.join(DataDirectoryPath.get_data_source_path(), data_link.alias)
    file_type = data_link.alias.split('.')[-1]
    sheet_names = ""
    if file_type in ['xlsx','xls', 'excel', 'EXCEL']:
        x1 = pd.ExcelFile(path)
        sheet_names = x1.sheet_names
    else:
        sheet_names = data_link.name

    catalogs = []
    catas = DataSourceCatalog.query.all()
    for catalog in catas:
        catalogs.append({"name": catalog.name, "catalog_id": catalog.id})

    name = data_link.name
    alias = data_link.alias
    data_link = {"name": name, "data_id": data_link_id, "data_type": "EXCEL", "create_time": "2019-02",
                 "creator": "wangw"}

    sheet_data = []
    if file_type in ['xlsx','xls', 'excel', 'EXCEL']:
        for s in range(len(sheet_names)):
            sheet_data.append({"num": s, "sheet_name": sheet_names[s], "sheet_id": ""})
    else:
        sheet_data.append({"num": 0, "sheet_name": sheet_names, "sheet_id": ""})

    sheet_list = {}
    sheet_list['data'] = sheet_data
    sheet_list['code'] = 0
    sheet_list['msg'] = "SUCCESS"
    sheet_list['data_id'] = data_link_id
    file_url = url_for('main.showimg_view', filename=alias, _external=True)
    global FILE_FOLDER
    FILE_FOLDER = DataDirectoryPath.get_data_source_path()
    # download_path = {'path': path}
    return render_template("file-conn.html", data_link=data_link, catalogs=catalogs, sheets=sheet_list, path=file_url)
