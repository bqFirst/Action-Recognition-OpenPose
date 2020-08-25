#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/8 9:22
# @Author : wangweimin
# @File   : v_task.py
# @Desc   :


import pandas as pd
from flask import json, send_from_directory
from flask import request, jsonify, render_template

from app.main.main import main
from app.main.services.operator.task_operator.task_operator import task_create_service, \
    get_tasks_info, get_task_result_data_service, task_delete_service, get_task_result_data_addr
from app.models import User

DOWN_FOLDER = '/data/upload'


# @main.route('/showimg/<filename>')
# def showimg_view(filename):
#     return send_from_directory(DOWN_FOLDER, filename)
@main.route('/application/task/create', methods=['POST'])
def task_create():
    user_id = User.query.first().id  # request.form['user_id']
    application_id = int(request.form['application_id'])
    description: str = request.form['description']
    data_link_id = int(request.form['data_link_id'])
    try:
        task_create_service(user_id=int(user_id), description=description, application_id=application_id,
                            data_link_id=data_link_id)
        return jsonify({'code': 0, 'msg': 'success'})
    except Exception as e:
        return jsonify({'code': 1, 'msg': str(e)})


@main.route('/application/task/delete', methods=['POST'])
def task_delete():
    application_id: int = int(request.form['application_id'])
    task_id: list = [int(request.form['task_id'])]
    try:
        task_delete_service(application_id=application_id, task_id=task_id)
        return jsonify({'code': 0, 'msg': 'success'})
    except Exception as e:
        return jsonify({'code': 1, 'msg': str(e)})


@main.route('/application/task/modify', methods=['POST'])
def task_modify():
    return jsonify({})


@main.route('/application/task/get/info', methods=['GET'])
def task_get_info():
    application_id = request.values.get('application_id')
    result = {}
    data: list = get_tasks_info(application_id=int(application_id))
    result['code'] = 0
    result['msg'] = ''
    result['data'] = data
    result['count'] = len(data)
    return json.dumps(result)


@main.route('/task')
def app():
    """主页视图"""
    return render_template("application.html")


@main.route('/application/task/get/result', methods=['GET'])
def get_result_data():
    result_file_id = request.values.get('id') or 1
    data = get_task_result_data_service(result_file_id=int(result_file_id))
    result = dict()
    result['code'] = 0
    result['msg'] = ''
    if isinstance(data, str):
        result['count'] = 0
        result['data'] = data
    elif isinstance(data, pd.DataFrame):
        result['count'] = data.shape[0]
        result['data'] = data.to_json(orient='records')
    else:
        result['count'] = 0
        result['data'] = 'Read data Error!'

    # imgUrl = url_for('ds/showimg_view', filename=filename, _external=True)

    return jsonify(result)


@main.route('/application/task/download/result', methods=['GET'])
def download_result_data():
    result_file_id = int(request.values.get('id'))
    application_dir, filename = get_task_result_data_addr(result_file_id=result_file_id)
    return send_from_directory(application_dir, filename, as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载
