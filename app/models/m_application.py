#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/17 11:00
# @Author : wangweimin
# @File   : m_application.py
# @Desc   :

from app import db
from datetime import datetime


class ApplicationCatalog(db.Model):
    __tablename__ = 't_application_catalogs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    pid = db.Column(db.Integer, default=0, nullable=False)

    # 外键
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))

    applications = db.relationship('Application', backref='catalog', lazy='dynamic')

    def __repr__(self):
        return '<project catalog: {}>'.format(self.name)


application_model_association_table = db.Table('t_mapping__application_model',
                                               db.Column('application_id', db.Integer,
                                                         db.ForeignKey('t_applications.id')),
                                               db.Column('model_id', db.Integer, db.ForeignKey('t_models.id'))
                                               )

application_ds_data_link_association_table = db.Table('t_mapping__application_data_link',
                                                      db.Column('application_id', db.Integer,
                                                                db.ForeignKey('t_applications.id')),
                                                      db.Column('data_link_id', db.Integer,
                                                                db.ForeignKey('t_data_source_data_links.id'))
                                                      )

application_data_excel_association_table = db.Table('t_mapping__application_data_excel',
                                                    db.Column('application_id', db.Integer,
                                                              db.ForeignKey('t_applications.id')),
                                                    db.Column('excel_data_id', db.Integer,
                                                              db.ForeignKey('t_data_source_excel_sheets.id'))
                                                    )

application_picture_catalog_association_table = db.Table('t_mapping__application_picture_catalog',
                                                         db.Column('application_id', db.Integer,
                                                                   db.ForeignKey('t_applications.id')),
                                                         db.Column('picture_catalog_id', db.Integer,
                                                                   db.ForeignKey('t_picture_catalogs.id'))
                                                         )

application_database_data_association_table = db.Table('t_mapping__application_database_data',
                                                       db.Column('application_id', db.Integer,
                                                                 db.ForeignKey('t_applications.id')),
                                                       db.Column('database_data_id', db.Integer,
                                                                 db.ForeignKey('t_database_datas.id'))
                                                       )


class Application(db.Model):
    __tablename__ = 't_applications'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    # 外键
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))
    catalog_id = db.Column(db.Integer, db.ForeignKey('t_application_catalogs.id'))
    container_id = db.Column(db.Integer, db.ForeignKey('t_docker_containers.id'))
    application_image_id = db.Column(db.Integer, db.ForeignKey('t_image_files.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('t_application_status.id'), default=1)

    tasks = db.relationship('Task', backref='application', lazy='dynamic')
    models = db.relationship('Model', secondary=application_model_association_table,
                             backref=db.backref('applications', lazy='dynamic'), lazy='dynamic')
    data_links = db.relationship('DataSourceDataLink', secondary=application_ds_data_link_association_table,
                                 backref=db.backref('applications', lazy='dynamic'), lazy='dynamic')
    excel_data = db.relationship('DataSourceExcelSheet', secondary=application_data_excel_association_table,
                                 backref=db.backref('applications', lazy='dynamic'), lazy='dynamic')
    picture_catalogs = db.relationship('PictureCatalog', secondary=application_picture_catalog_association_table,
                                       backref=db.backref('applications', lazy='dynamic'), lazy='dynamic')
    database_data = db.relationship('DatabaseData', secondary=application_database_data_association_table,
                                    backref=db.backref('applications', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<application: {}>'.format(self.name)

    @property
    def status(self):
        return self.application_status

    @property
    def port(self):
        return self.container.port
