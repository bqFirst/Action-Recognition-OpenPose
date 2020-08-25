#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/17 10:58
# @Author : wangweimin
# @File   : m_project.py
# @Desc   :

from app import db
from datetime import datetime


class ProjectCatalog(db.Model):
    __tablename__ = 't_project_catalogs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    pid = db.Column(db.Integer, default=0, nullable=False)

    # 外键
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))

    projects = db.relationship('Project', backref='catalog', lazy='dynamic')

    def __repr__(self):
        return '<project catalog: {}>'.format(self.name)


class Project(db.Model):
    __tablename__ = 't_projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    modify_time = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(120), nullable=True, default='')
    # 外键
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))
    modifier_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))
    catalog_id = db.Column(db.Integer, db.ForeignKey('t_project_catalogs.id'))

    models = db.relationship('Model', backref='project', lazy='dynamic')
    process_data = db.relationship('ProjectProcessData', backref='project', lazy='dynamic')
    # excel_data = db.relationship('DataSourceExcelSheet', backref='project', lazy='dynamic')
    edit_window = db.relationship('ProjectEditWindow', backref='project', lazy='dynamic')
    # database_data = db.relationship('DatabaseData', backref='project', lazy='dynamic')

    def __repr__(self):
        return '<project: {}>'.format(self.name)


class ProjectEditWindow(db.Model):
    __tablename__ = 't_project_edit_windows'
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(128), nullable=False)

    # 外键
    project_id = db.Column(db.Integer, db.ForeignKey('t_projects.id'))

    def __repr__(self):
        return '<project edit window of project: {}>'.format(self.name, self.project.name)


class ProjectProcessData(db.Model):
    __tablename__ = 't_project_process_datas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    alias = db.Column(db.String(128), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    record = db.Column(db.Integer)

    # 外键
    project_id = db.Column(db.Integer, db.ForeignKey('t_projects.id'))
    data_type_id = db.Column(db.Integer, db.ForeignKey('t_data_types.id'))

    def __repr__(self):
        return '<project process data: {} of project: {}>'.format(self.name, self.project.name)

    @property
    def type(self):
        return self.data_type.data_type
