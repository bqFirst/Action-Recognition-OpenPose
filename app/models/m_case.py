#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/1/19 14:58
# @Author : wangweimin
# @File   : m_case.py
# @Desc   :


from app import db
from datetime import datetime


class CaseCatalog(db.Model):
    __tablename__ = 't_case_catalogs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    pid = db.Column(db.Integer, default=0, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    # 外键
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))

    cases = db.relationship('Case', backref='catalog', lazy='dynamic')

    def __repr__(self):
        return '<case catalog: {}>'.format(self.name)


class CaseInfo(db.Model):
    __tablename__ = 't_cases_info'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False, default='')
    scene = db.Column(db.String(500), nullable=False, default='')
    data_trained = db.Column(db.String(500), nullable=False, default='')
    data_treatment = db.Column(db.String(500), nullable=False, default='')
    model_algorithm = db.Column(db.String(500), nullable=False, default='')
    model_trained = db.Column(db.String(500), nullable=False, default='')

    cases = db.relationship('Case', backref='info', lazy='dynamic')

    def __repr__(self):
        return '<info of case: {}>'.format(self.cases.first().name)


class Case(db.Model):
    __tablename__ = 't_cases'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    key = db.Column(db.String(128), nullable=False, unique=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    # 外键
    catalog_id = db.Column(db.Integer, db.ForeignKey('t_case_catalogs.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))
    container_id = db.Column(db.Integer, db.ForeignKey('t_case_docker_containers.id'))
    case_info_id = db.Column(db.Integer, db.ForeignKey('t_cases_info.id'))

    def __repr__(self):
        return '<case: {}>'.format(self.name)

    @property
    def port(self):
        return self.container.port
