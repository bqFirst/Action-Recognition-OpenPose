#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/7/30 10:17
# @Author : wangweimin
# @File   : __init__.py.py
# @Desc   :

from flask import Flask
from conf.base_config import config
# from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from flask_mail import Mail, Message

# 数据库映射
db = SQLAlchemy()

# Web socket
async_mode = None
socketio = SocketIO()

#
# login = LoginManager()
# bootstrap = Bootstrap()

# mail = Mail()


def create_app(config_name='default'):
    # 创建app应用,__name__是python预定义变量，被设置为使用本模块.
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # api接口文档
    from flasgger import Swagger
    Swagger(app)

    # bootstrap.init_app(app)

    # login.init_app(app)
    # login.login_view = 'main.login'  # !!!!!登录限制，若无登录，则跳转到指定的url

    # from .app_1_0 import api as api_1_0_blueprint
    # app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1000')
    # url_prefix 为网址前缀

    from app.main.main import main
    app.register_blueprint(main)

    # 建立数据库关系
    db.init_app(app)

    # Web Socket
    socketio.init_app(app, async_mode=async_mode)

    # 邮箱
    # mail.init_app(app)

    return app


from app import models
