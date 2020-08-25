#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/20 16:39
# @Author : wangweimin
# @File   : run.py
# @Desc   :

import importlib
import pandas as pd
import joblib
import json
# import traceback
from flask import Flask, request, jsonify
from sklearn.pipeline import Pipeline

from app.main.modeling import IModelPredict
from conf.data_path import DataDName, ModelDName, ModelFileDName, ModelSrcDName

import sys
import os
cur_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_path)


app = Flask(__name__)
ModelInfoMap: dict = None  # {'model_name': {'file': '...', 'src': '...', 'type': '..'}}
ModelMap: dict = dict()
ModelPredictMap: dict = dict()
ModelMapFileName = 'model_mapping.json'
InitErrorMsg: str = None


@app.route('/predict', methods=['POST'])
def predict():
    if InitErrorMsg:
        return jsonify({'code': 1, 'message': {'Error': 'init error\n' + InitErrorMsg}})
    try:
        # 上传数据获取
        try:
            data = request.form['data']
            data: pd.DataFrame = pd.DataFrame(json.loads(data))
        except KeyError:
            try:
                f = request.files['file']
            except KeyError:
                raise ValueError('Require parameter \'file\'')
            try:
                data = pd.read_csv(f)
            except Exception:
                raise ValueError('File parsing failed')
        model = request.args.get('model')

        # 模型预测
        data = model_predict(data, model=model)

        return jsonify({'data': data.to_dict(orient='records'), 'code': 0})
    except Exception as e:
        return jsonify({'code': 1, 'message': {'Error': str(e)}})


@app.route('/init_status', methods=['GET'])
def init_status():
    if InitErrorMsg:
        return jsonify({'code': 1, 'message': {'Error': InitErrorMsg}})
    return jsonify({'code': 0})


# 模型加载
def init_model():
    global ModelMap
    directory = os.path.join(cur_path, DataDName, ModelDName, ModelFileDName)
    for model_name, model_info in ModelInfoMap.items():
        file_name = os.path.join(directory, model_info[ModelFileDName])
        with open(file_name, 'rb') as f:
            model: Pipeline = joblib.load(f)
        if model is None:
            raise ValueError('Model {} load failed!'.format(model_name))
        ModelMap[model_name] = model


def model_predict(data: pd.DataFrame, model: str) -> pd.DataFrame:
    if model is None:
        raise ValueError('Require parameter \'model\'')
    model_predict_object = ModelPredictMap.get(model)
    if model_predict_object is None:
        raise ValueError('Model {} does not exist'.format(model))
    result = model_predict_object.predict(data)
    return pd.DataFrame(result, columns=['result'])


# 用户自定义模型预测加载
def init_predict_model():
    global ModelPredictMap
    global ModelMap
    package = os.path.join(DataDName, ModelDName, ModelSrcDName)
    for model_name, model_info in ModelInfoMap.items():
        model_src_name = model_info[ModelSrcDName]
        module = importlib.import_module(
            '.'.join(os.path.join(package, model_src_name.rstrip('.py')).split(os.path.sep)))

        model_predict_object: IModelPredict = None
        if hasattr(module, 'ModelPredict'):
            model_predict_class = getattr(module, 'ModelPredict')
            model_predict_object: IModelPredict = model_predict_class(ModelMap[model_name])
        if model_predict_object is None:
            raise ValueError('ModelPredict load failed!')
        ModelPredictMap[model_name] = model_predict_object


def init_model_map():
    global ModelInfoMap
    with open(ModelMapFileName, 'r') as f:
        ModelInfoMap = json.load(f)


def init():
    # noinspection PyBroadException
    try:
        init_model_map()
        init_model()
        init_predict_model()
    except Exception:
        global InitErrorMsg
        import traceback
        InitErrorMsg = traceback.format_exc()


if __name__ == '__main__':
    init()
    app.run(host='0.0.0.0')
