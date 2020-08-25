#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/30 14:14
# @Author : wangweimin
# @File   : m_message.py
# @Desc   :

from app import db


##########################
# 数据文件
##########################
class DataType(db.Model):
    __tablename__ = 't_data_types'
    id = db.Column(db.Integer, primary_key=True)
    data_type = db.Column(db.String(11), nullable=False)  # {1: 'csv', 2: 'excel', 3: 'picture', 4: 'txt', 5: 'json'}

    data_source_data_link = db.relationship('DataSourceDataLink', backref='data_type', lazy='dynamic')
    data_predicted_data_link = db.relationship('DataPredictedDataLink', backref='data_type', lazy='dynamic')
    project_process_data_link = db.relationship('ProjectProcessData', backref='data_type', lazy='dynamic')

    def __repr__(self):
        return '<data file type: {}>'.format(self.data_type)


##########################
# 数据库
##########################
class DatabaseType(db.Model):
    __tablename__ = 't_database_types'
    id = db.Column(db.Integer, primary_key=True)
    db_type = db.Column(db.String(20))  # {1: 'mysql'}

    database = db.relationship('Database', backref='db_type', lazy='dynamic')

    def __repr__(self):
        return '<database type: {}>'.format(self.db_type)


##########################
# 模型
##########################
class ModelType(db.Model):
    __tablename__ = 't_model_types'
    id = db.Column(db.Integer, primary_key=True)
    model_type = db.Column(db.String(20), nullable=False)  # {1: 'sklearn', 2: 'tensorflow'}

    model_version = db.relationship('ModelVersion', backref='model_type', lazy='dynamic')

    def __repr__(self):
        return '<model type: {}>'.format(self.model_type)


class ModelStatus(db.Model):
    __tablename__ = 't_model_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)  # {1: '生成失败', 2: '生成成功', 3: '正在生成'}

    model_version = db.relationship('ModelVersion', backref='model_status', lazy='dynamic')

    # task = db.relationship('Task', backref='model_status', lazy='dynamic')

    def __repr__(self):
        return '<status: {}>'.format(self.name)


##########################
# 报错信息
##########################
class ErrorMessage(db.Model):
    __tablename__ = 't_error_messages'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), default='')

    def __repr__(self):
        return '<Error message: {}>'.format(self.message)


##########################
# 返回状态码说明
##########################
class ResponseCode(db.Model):
    __tablename__ = 't_code_descriptions'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Code {}: {}>'.format(self.code, self.description)


##########################
# 应用
##########################
class ApplicationStatus(db.Model):
    __tablename__ = 't_application_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)  # {1: '服务中', 2: '未启动', 3: '启动中', 4: '停止中'}

    application = db.relationship('Application', backref='application_status', lazy='dynamic')

    def __repr__(self):
        return '<Application status {}>'.format(self.name)


class TaskStatus(db.Model):
    __tablename__ = 't_task_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)  # {1: '运行中', 2: '停止中', 3: '已停止', 4: '运行成功', 5: '运行失败'}

    task = db.relationship('Task', backref='task_status', lazy='dynamic')

    def __repr__(self):
        return '<Task status {}>'.format(self.name)


class TaskType(db.Model):
    __tablename__ = 't_task_types'
    id = db.Column(db.Integer, primary_key=True)
    task_type = db.Column(db.String(20),
                          nullable=False)  # {1: '离线excel', 2: '离线picture', 3: '离线database_data', 4: '离线非excel'}

    task = db.relationship('Task', backref='task_type', lazy='dynamic')

    def __repr__(self):
        return '<model type: {}>'.format(self.task_type)


##########################
# 镜像、容器
##########################
class DockerImageStatus(db.Model):
    __tablename__ = 't_docker_image_status'
    id = db.Column(db.Integer, primary_key=True)
    image_status = db.Column(db.String(20), nullable=False)  # {1: '未打包', 2: '打包中', 3: '打包成功'}

    images = db.relationship('DockerImage', backref='image_status', lazy='dynamic')
    application_images = db.relationship('DockerImageFile', backref='image_status', lazy='dynamic')

    def __repr__(self):
        return '<image type: {}>'.format(self.image_status)


class BaseDockerImage(db.Model):
    __tablename__ = 't_docker_base_images'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)  # {1: 'flask-sklearn', 2: 'flask-tensorflow'}  对应ModelType

    # {1: 'flask-sklearn/centos7:latest', 2: 'flask-tensorflow/centos7:latest'}
    tags = db.Column(db.String(50), nullable=False, default='')
    alias = db.Column(db.String(128))

    containers = db.relationship('DockerContainer', backref='base_image', lazy='dynamic')

    def __repr__(self):
        return '<base image: {}>'.format(self.name)


class ParamType(db.Model):
    __tablename__ = 't_param_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)  # {1: 'picture', 2: 'json', 3: 'float', 4: 'int',
    #  5: 'video'}

    input_param = db.relationship('InputParam', backref='param_type', lazy='dynamic')
    output_param = db.relationship('OutputParam', backref='param_type', lazy='dynamic')

    def __repr__(self):
        return '<base image: {}>'.format(self.name)
