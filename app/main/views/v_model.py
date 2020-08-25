#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/13 15:27
# @Author : wangweimin
# @File   : v_model.py
# @Desc   :

import traceback
from flask import request, jsonify
from sklearn.pipeline import Pipeline

from app.main.main import main
from app.main.services.operator.model_operator.model_operator import model_train_service, model_create_service, model_save_service, \
    model_src_preserve_service
from app.models import *


@main.route('/project/model_operator/create', methods=['POST'])
def model_create():
    res = dict(code=-1, msg=None)
    model_name = request.form['model_name']
    user_id = int(request.form['user_id'])
    project_id = int(request.form['project_id'])
    try:
        model_create_service(project_id=project_id, model_name=model_name, user_id=user_id, description='')
        res.update(code=0, msg='Success')
    except Exception as e:
        res.update(msg=str(e))
    return jsonify(res)


@main.route('/project/model_operator/src_preserve', methods=['POST'])
def model_src_preserve():
    res = dict(code=-1, msg=None)
    # user_id = request.form['user_id']
    user_id = User.query.first().id  # int(request.form['user_id'])
    model_id = int(request.form['model_id'])
    new_src = request.form['src']
    try:
        model_src_preserve_service(model_id=model_id, user_id=user_id, new_src=new_src)
        res.update(code=0, msg='Success')
    except Exception as e:
        res.update(msg=str(e))
    return jsonify(res)


@main.route('/project/model_operator/train', methods=['POST'])
def model_train():
    res = dict(code=-1, msg=None)
    model_id = request.form['model_id']
    pipe: Pipeline = model_train_service(model_id=int(model_id))
    try:
        status: bool = model_save_service(model_id=model_id, pipe=pipe)
        if status:
            res.update(code=0, msg='success')
        else:
            res.update(msg='Train Error')
    except Exception as e:
        res.update(msg=str(e) + '\n' + traceback.format_exc())
    return jsonify(res)
