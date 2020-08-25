#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/7/30 11:03
# @Author : wangweimin
# @File   : base_config.py
# @Desc   :

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BasicConfig(object):
    SECRET_KEY = 'a2389dfjsk@#sd#a'

    # 格式为mysql+pymysql://数据库用户名:密码@数据库地址:端口号/数据库的名字?数据库格式
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user1:123456@localhost:3306/flask_blog?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # MAIL_SERVER = 'smtp.qq.com'
    # MAIL_PORT = 465
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # MAIL_DEFAULT_SENDER = '1169586839@11.com'  # 默认发送者
    # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'  # 文件标题前缀

    # ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    # MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    CELERY_BROKER_URL = 'redis://:123456@127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://:123456@127.0.0.1:6379/0'
    CELERY_TASK_SERIALIZER = 'json'

    @staticmethod
    def init_app(app):
        pass


# 开发环境
class DevelopmentConfig(BasicConfig):

    DIALECT = 'mysql'  # 要用的什么数据库
    DRIVER = 'pymysql'  # 连接数据库驱动
    USERNAME = 'ramadidb'  # 用户名
    PASSWORD = 'gPu13py6_Z7g7w5V'  # 密码
    HOST = '36.111.42.18'  # 服务器
    # HOST = '127.0.0.1'  # 服务器
    PORT = '3306'  # 端口
    # PORT = '13306'  # 端口
    DATABASE = 'ramadidb'  # 数据库名
    JSON_AS_ASCII = False

    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user1:123456@localhost:3306/flask_blog?charset=utf8'
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )

    CELERY_BROKER_URL = 'redis://:123456@127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://:123456@127.0.0.1:6379/0'
    CELERY_TASK_SERIALIZER = 'json'


# 测试环境
class TestingConfig(BasicConfig):
    """
    仅在数据库测试使用
    """
    TESTING = True

    DIALECT = 'mysql'  # 要用的什么数据库
    DRIVER = 'pymysql'  # 连接数据库驱动
    USERNAME = 'root'  # 用户名
    PASSWORD = '123456'  # 密码
    HOST = '127.0.0.1'  # 服务器
    PORT = '3306'  # 端口
    DATABASE = 'ramadidb'  # 数据库名
    JSON_AS_ASCII = False

    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user1:123456@localhost:3306/flask_blog?charset=utf8'
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )

    CELERY_BROKER_URL = 'redis://:123456@127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://:123456@127.0.0.1:6379/0'
    CELERY_TASK_SERIALIZER = 'json'


# 生产环境
class ProductionConfig(BasicConfig):
    DIALECT = 'mysql'  # 要用的什么数据库
    DRIVER = 'pymysql'  # 连接数据库驱动
    USERNAME = 'ramadidb'  # 用户名
    PASSWORD = 'gPu13py6_Z7g7w5V'  # 密码
    HOST = '172.16.0.194'  # 服务器
    PORT = '3306'  # 端口
    DATABASE = 'ramadidb'  # 数据库名
    JSON_AS_ASCII = False

    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user1:123456@localhost:3306/flask_blog?charset=utf8'
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )

    CELERY_BROKER_URL = 'redis://:123456@127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://:123456@127.0.0.1:6379/0'
    CELERY_TASK_SERIALIZER = 'json'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
