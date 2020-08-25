#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/12 11:39
# @Author : wangweimin
# @File   : m_database.py
# @Desc   :

from datetime import datetime

from app import db


class Database(db.Model):
    __tablename__ = 't_databases'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    ip = db.Column(db.String(15))
    port = db.Column(db.String(5))
    user = db.Column(db.String(20))
    password = db.Column(db.String(30))
    database = db.Column(db.String(30))
    description = db.Column(db.String(50))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    # 外键
    db_type_id = db.Column(db.Integer, db.ForeignKey('t_database_types.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))

    data = db.relationship('DatabaseData', backref='database', lazy='dynamic')

    def __repr__(self):
        return '<database: {}>'.format(self.name)

    def show_name(self) -> str:
        return '{} ({}: {}:{})'.format(self.name, self.db_type.db_type, self.ip, self.port)

    @property
    def type(self):
        return self.db_type.db_type


database_data_project_association_table = db.Table('t_mapping__database_data_project',
                                                   db.Column('database_data_id', db.Integer,
                                                             db.ForeignKey('t_database_datas.id')),
                                                   db.Column('project_id', db.Integer, db.ForeignKey('t_projects.id'))
                                                   )


class DatabaseData(db.Model):
    __tablename__ = 't_database_datas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    alias = db.Column(db.String(50))
    sql = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_used = db.Column(db.Boolean, default=False)
    record = db.Column(db.Integer)

    # 外键
    database_id = db.Column(db.Integer, db.ForeignKey('t_databases.id'))
    # project_id = db.Column(db.Integer, db.ForeignKey('t_projects.id'))
    data_overview_id = db.Column(db.Integer, db.ForeignKey('t_data_overviews.id'))

    projects = db.relationship('Project', secondary=database_data_project_association_table,
                               backref=db.backref('database_data', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<database data: {}>'.format(self.name)

    @property
    def type(self):
        return self.database.type

    @property
    def project(self):
        return self.projects.first()

    @property
    def application(self):
        return self.applications.first()

    @property
    def creator(self):
        return self.database.creator
