#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/5 10:50
# @Author : wangwei
# @File   : run_tf.py
# @Desc   :

import importlib
import io
import json
import os
import sys
import traceback

import pandas as pd
import tensorflow as tf
from PIL import Image
from flask import Flask, request, jsonify
from tensorflow.python.platform import gfile

from app.main.modeling import IModelPredict
from conf.data_path import DataDName, ModelDName, ModelFileDName, ModelSrcDName

cur_path = os.path.abspath(os.path.dirname(__file__))

sys.path.append(cur_path)


app = Flask(__name__)
ModelPredict: IModelPredict = None


@app.route('/predict', methods=['POST'])
def predict():
    result = dict()
    try:
        images = []
        data = request.files.getlist('data')
        for i in range(len(data)):
            image = Image.open(io.BytesIO(data[i].read()))
            images.append(image)

        data = model_predict(images)

        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data, columns=['result'])
        result.update(data=data.to_dict(orient='records'))
    except Exception as e:
        result.update(message=traceback.format_exc())
    return json.dumps(result)


@app.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'success'})


def init_model():
    global sess
    global graph_def
    sess = tf.Session()
    directory = os.path.join(cur_path, DataDName, ModelDName, ModelFileDName)
    file_name = os.listdir(directory)[0]
    with gfile.FastGFile(os.path.join(directory, file_name), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        sess.graph.as_default()
        tf.import_graph_def(graph_def, name='')
        sess.run(tf.global_variables_initializer())

    if sess is None:
        raise ValueError('Model load failed!')


def model_predict(data) -> pd.DataFrame:

    return ModelPredict.predict(data)


# 用户自定义模型预测加载
def init_predict_model():
    global ModelPredict
    model_src_name = os.listdir(os.path.join(cur_path, DataDName, ModelDName, ModelSrcDName))[0]
    module = importlib.import_module(
        '.'.join(os.path.join(DataDName, ModelDName, ModelSrcDName, model_src_name.rstrip('.py')).split(os.path.sep)))
    if hasattr(module, 'ModelPredict'):
        model_predict_class = getattr(module, 'ModelPredict')
        ModelPredict = model_predict_class([sess, graph_def])
    if ModelPredict is None:
        raise ValueError('ModelPredict load failed!')


if __name__ == '__main__':
    init_model()
    init_predict_model()
    app.run(host='0.0.0.0')
