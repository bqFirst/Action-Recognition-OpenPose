#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/17 10:57
# @Author : wangweimin
# @File   : m_data_source.py
# @Desc   :

from app import db
from datetime import datetime


class DataSourceCatalog(db.Model):
    __tablename__ = 't_data_source_catalogs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    pid = db.Column(db.Integer, default=0, nullable=False)

    # 外键
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))

    data_links = db.relationship('DataSourceDataLink', backref='catalog', lazy='dynamic')

    def __repr__(self):
        return '<data source catalog: {}>'.format(self.name)


class DataOverview(db.Model):
    __tablename__ = 't_data_overviews'
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(50))

    data_link = db.relationship('DataSourceDataLink', backref='data_overview', lazy='dynamic')
    excel_sheets = db.relationship('DataSourceExcelSheet', backref='data_overview', lazy='dynamic')
    database_data = db.relationship('DatabaseData', backref='data_overview', lazy='dynamic')

    def __repr__(self):
        return '<data overview of {}>'.format(self.data_link.first().name)


data_link_project_association_table = db.Table('t_mapping__data_link_project',
                                               db.Column('data_link_id', db.Integer,
                                                         db.ForeignKey('t_data_source_data_links.id')),
                                               db.Column('project_id', db.Integer, db.ForeignKey('t_projects.id'))
                                               )


class DataSourceDataLink(db.Model):
    __tablename__ = 't_data_source_data_links'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    alias = db.Column(db.String(50))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_used = db.Column(db.Boolean, default=False)
    record = db.Column(db.Integer)

    # 外键
    data_type_id = db.Column(db.Integer, db.ForeignKey('t_data_types.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))
    catalog_id = db.Column(db.Integer, db.ForeignKey('t_data_source_catalogs.id'))
    data_overview_id = db.Column(db.Integer, db.ForeignKey('t_data_overviews.id'))

    projects = db.relationship('Project', secondary=data_link_project_association_table,
                               backref=db.backref('data_links', lazy='dynamic'), lazy='dynamic')
    excel_sheets = db.relationship('DataSourceExcelSheet', backref='data_link', lazy='dynamic')

    def __repr__(self):
        return '<data source data link: {}>'.format(self.name)

    @property
    def type(self):
        return self.data_type.data_type

    @property
    def application(self):
        return self.applications.first()


data_excel_project_association_table = db.Table('t_mapping__excel_data_project',
                                                db.Column('excel_data_id', db.Integer,
                                                          db.ForeignKey('t_data_source_excel_sheets.id')),
                                                db.Column('project_id', db.Integer, db.ForeignKey('t_projects.id'))
                                                )


class DataSourceExcelSheet(db.Model):
    __tablename__ = 't_data_source_excel_sheets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    alias = db.Column(db.String(50))
    is_used = db.Column(db.Boolean, default=False)
    record = db.Column(db.Integer)

    # 外键
    data_link_id = db.Column(db.Integer, db.ForeignKey('t_data_source_data_links.id'))
    data_overview_id = db.Column(db.Integer, db.ForeignKey('t_data_overviews.id'))
    # project_id = db.Column(db.Integer, db.ForeignKey('t_projects.id'))

    projects = db.relationship('Project', secondary=data_excel_project_association_table,
                               backref=db.backref('excel_data', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<sheet {} of data source data link: {}>'.format(self.name, self.data_link.name)

    @property
    def type(self):
        return 'excel'

    @property
    def project(self):
        return self.projects.first()

    @property
    def application(self):
        return self.applications.first()
