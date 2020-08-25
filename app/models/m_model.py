#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/17 10:59
# @Author : wangweimin
# @File   : m_model.py
# @Desc   :

from app import db
from datetime import datetime


class Model(db.Model):
    __tablename__ = 't_models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    modify_time = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(120), default='')
    # 外键
    project_id = db.Column(db.Integer, db.ForeignKey('t_projects.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))

    model_version = db.relationship('ModelVersion', backref='model', lazy='dynamic')
    tasks = db.relationship('Task', backref='model', lazy='dynamic')

    def __repr__(self):
        return '<model: {}>'.format(self.name)


class ModelInfo(db.Model):
    __tablename__ = 't_model_infos'
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(128), nullable=False)

    model_version = db.relationship('ModelVersion', backref='model_info', lazy='dynamic')

    def __repr__(self):
        return '<model output file: {}>'.format(self.alias)


class ModelSourceCode(db.Model):
    __tablename__ = 't_model_source_codes'
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(128), nullable=False)

    model_version = db.relationship('ModelVersion', backref='model_source_code', lazy='dynamic')

    def __repr__(self):
        return '<model src code file: {}>'.format(self.alias)


class ModelFile(db.Model):
    __tablename__ = 't_model_files'
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(128), nullable=False)

    model_version = db.relationship('ModelVersion', backref='model_file', lazy='dynamic')

    def __repr__(self):
        return '<model file: {}>'.format(self.alias)


class ModelDataFormat(db.Model):
    __tablename__ = 't_model_data_formats'
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(128), nullable=False)

    model_version = db.relationship('ModelVersion', backref='data_format', lazy='dynamic')


class ModelPackage(db.Model):
    __tablename__ = 't_model_packages'
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(128), nullable=False)

    model_version = db.relationship('ModelVersion', backref='model_package', lazy='dynamic')

    def __repr__(self):
        return '<model package: {}>'.format(self.alias)


class ModelVersion(db.Model):
    __tablename__ = 't_model_versions'
    id = db.Column(db.Integer, primary_key=True)

    # 外键
    status_id = db.Column(db.Integer, db.ForeignKey('t_model_status.id'), default=3)
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('t_models.id'))
    model_source_code_id = db.Column(db.Integer, db.ForeignKey('t_model_source_codes.id'))
    model_info_id = db.Column(db.Integer, db.ForeignKey('t_model_infos.id'))
    model_file_id = db.Column(db.Integer, db.ForeignKey('t_model_files.id'))
    data_format_id = db.Column(db.Integer, db.ForeignKey('t_model_data_formats.id'))
    image_id = db.Column(db.Integer, db.ForeignKey('t_docker_images.id'))
    model_type_id = db.Column(db.Integer, db.ForeignKey('t_model_types.id'))
    model_package_id = db.Column(db.Integer, db.ForeignKey('t_model_packages.id'))

    def __repr__(self):
        return '<model version of {}>'.format(self.model.name)

    @property
    def name(self):
        return self.model.name
