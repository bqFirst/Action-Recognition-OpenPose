#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/7/30 10:56
# @Author : wangwei
# @File   : v_application.py
# @Desc   :

import traceback
from flask import request, jsonify

from app.main.main import main
from app.main.services.operator.application_operator.application_operator import application_create_service
from app.models import User


@main.route("/application/create", methods=['POST'])
def application_create():
    """主页视图"""
    user_id = User.query.first().id  # request.form['user_id']
    catalog_id = int(request.form['application_catalog_id'])
    application_name = request.form['application_name']
    model_id = int(request.form['model_id'])
    try:
        application_create_service(application_name=application_name, model_id=model_id, user_id=user_id,
                                   catalog_id=catalog_id)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': traceback.format_exc()})
