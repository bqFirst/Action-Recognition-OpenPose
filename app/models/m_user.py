#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/17 10:56
# @Author : wangweimin
# @File   : m_user.py
# @Desc   :

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    __tablename__ = 't_users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    telephone = db.Column(db.String(11))

    project_create = db.relationship('Project', backref='creator', lazy='dynamic', foreign_keys='Project.creator_id')
    project_modify = db.relationship('Project', backref='modifier', lazy='dynamic', foreign_keys='Project.modifier_id')
    project_catalog = db.relationship('ProjectCatalog', backref='creator', lazy='dynamic')
    data_source_catalog = db.relationship('DataSourceCatalog', backref='creator', lazy='dynamic')
    data_application_catalog = db.relationship('ApplicationDataCatalog', backref='creator', lazy='dynamic')
    application_catalog = db.relationship('ApplicationCatalog', backref='creator', lazy='dynamic')
    models = db.relationship('Model', backref='creator', lazy='dynamic')
    model_versions = db.relationship('ModelVersion', backref='creator', lazy='dynamic')
    applications = db.relationship('Application', backref='creator', lazy='dynamic')
    tasks = db.relationship('Task', backref='creator', lazy='dynamic')
    data_source_data_link = db.relationship('DataSourceDataLink', backref='creator', lazy='dynamic')
    data_predicted_data_link = db.relationship('DataPredictedDataLink', backref='creator', lazy='dynamic')
    docker_image = db.relationship('DockerImage', backref='creator', lazy='dynamic')
    docker_container = db.relationship('DockerContainer', backref='creator', lazy='dynamic')
    picture_catalog = db.relationship('PictureCatalog', backref='creator', lazy='dynamic')
    database = db.relationship('Database', backref='creator', lazy='dynamic')
    case_catalog = db.relationship('CaseCatalog', backref='creator', lazy='dynamic')
    case = db.relationship('Case', backref='creator', lazy='dynamic')

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user_id = data.get('id')
        if user_id is not None and isinstance(user_id, int):
            user = User.query.get(user_id)
            return user
        return None

    def __repr__(self):
        return '<user: {}>'.format(self.name)
