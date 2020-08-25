#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/3/24 0024 16:10
# @Author : wangw
# @File   : run.py
# @Desc   :

import sys
import os

cur_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.split(cur_path)[0])

from flask import Flask, request, jsonify
from sort_action_recognition import Model

app = Flask(__name__)
InitErrorMsg: str = None


@app.route('/predict', methods=['POST'])
def predict():
    if InitErrorMsg:
        return jsonify({'code': 1, 'message': {'Error': 'init error\n' + InitErrorMsg}})

    try:
        # 上传数据获取
        try:
            mode_name = request.form['mode_name']
            mode: dict = Model.get_param(mode_name=mode_name)
            if not mode:
                raise ValueError('mode {} does not exists'.format(mode_name))
            params: list = mode.get('param').get('input')
            kwargs = dict()
            for param_ in params:
                param_name = param_['name']
                try:
                    kwargs[param_name] = request.form[param_name]
                except KeyError:
                    if param_['required']:
                        raise
            func = mode.get('func')
            func = getattr(Model, func)
        except KeyError:
            raise ValueError('Missing parameter')
        result: dict = func(**kwargs)
        result['code'] = 0
        return jsonify(result)
    except Exception as e:
        import traceback
        return jsonify({'code': 1, 'message': {'Error': traceback.format_exc()}})


@app.route('/init_status', methods=['GET'])
def init_status():
    if InitErrorMsg:
        return jsonify({'code': 1, 'message': {'Error': InitErrorMsg}})
    return jsonify({'code': 0})


@app.route('/param', methods=['GET'])
def param():
    if InitErrorMsg:
        return jsonify({'code': 1, 'message': {'Error': 'init error\n' + InitErrorMsg}})
    return jsonify(
        {'code': 0, 'param': Model.get_param(), 'name': Model.get_name(), 'assessment': Model.get_assessment(),
         'key': Model.get_key()})


def init():
    # noinspection PyBroadException
    try:
        Model.init()
    except Exception:
        global InitErrorMsg
        import traceback
        InitErrorMsg = traceback.format_exc()


if __name__ == '__main__':
    init()
    app.run(host='0.0.0.0', port=5000)
