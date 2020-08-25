#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/7 9:34
# @Author : wangweimin
# @File   : v_project.py
# @Desc   :

from flask import request, jsonify

from app.main.main import main
from app.main.services.operator.project_operator import project_create_service
from app.models import *


@main.route('/project/create', methods=['POST'])
def project_create():
    # Todo
    data_source_link_id = int(request.form['link_id'])
    user_id = User.query.first().id  # int(request.form['user_id'])
    catalog_id = int(request.form['project_catalog_id'])
    project_name = request.form['project_name']
    description = request.form['description']
    try:
        project_create_service(project_name=project_name, description=description, user_id=user_id,
                               data_links_id=[data_source_link_id], catalog_id=catalog_id)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': str(e)})
