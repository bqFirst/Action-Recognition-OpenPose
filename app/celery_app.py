#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/3/6 16:40
# @Author : wangweimin
# @File   : celery_app.py
# @Desc   :

from flask import Flask
from conf.base_config import config, BasicConfig
from conf.system_config import ServerAddress
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

# 数据库映射
db = SQLAlchemy()

# Web socket
async_mode = None
socketio = SocketIO()


# 异步框架
celery = Celery(__name__, broker=BasicConfig.CELERY_BROKER_URL, backend=BasicConfig.CELERY_RESULT_BACKEND)


def create_celery_app(config_name='default'):
    ServerAddress.init(config_name=config_name)
    app = Flask(__name__)  # create_app(config_name=config_name)
    app.config.from_object(config[config_name])
    celery.conf.update(app.config)
    db.init_app(app)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            # 将Flask App的上下文信息包含至Celery对象中
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return app
