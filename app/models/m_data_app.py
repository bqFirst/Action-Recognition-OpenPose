#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/8 10:31
# @Author : wangweimin
# @File   : m_data_app.py
# @Desc   : 该表不使用


from app import db
from datetime import datetime


class ApplicationDataCatalog(db.Model):
    __tablename__ = 't_application_data_catalogs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    pid = db.Column(db.Integer, default=0, nullable=False)

    # 外键
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))

    data_links = db.relationship('DataPredictedDataLink', backref='catalog', lazy='dynamic')

    def __repr__(self):
        return '<application data catalog: {}>'.format(self.name)


data_link_application_association_table = db.Table('t_mapping__data_link_application',
                                                   db.Column('data_link_id', db.Integer,
                                                             db.ForeignKey('t_data_predicted_data_links.id')),
                                                   db.Column('application_id', db.Integer,
                                                             db.ForeignKey('t_applications.id'))
                                                   )


class DataPredictedDataLink(db.Model):
    __tablename__ = 't_data_predicted_data_links'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    alias = db.Column(db.String(50))  # 数据为文件时，需要填充，否则填充以下数据库信息
    ip = db.Column(db.String(15))
    port = db.Column(db.String(5))
    user = db.Column(db.String(20))
    password = db.Column(db.String(30))
    database = db.Column(db.String(30))
    code = db.Column(db.String(15))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    # 外键
    data_type_id = db.Column(db.Integer, db.ForeignKey('t_data_types.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))
    catalog_id = db.Column(db.Integer, db.ForeignKey('t_application_data_catalogs.id'))
    # data_overview_id = db.Column(db.Integer, db.ForeignKey('t_data_overviews.id'))

    def __repr__(self):
        return '<data predicted data link: {}>'.format(self.name)
