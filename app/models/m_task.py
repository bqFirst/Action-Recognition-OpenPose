#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/17 11:01
# @Author : wangweimin
# @File   : m_task.py
# @Desc   :

from app import db
from datetime import datetime


class TaskResultFile(db.Model):
    __tablename__ = 't_task_results'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    alias = db.Column(db.String(128), nullable=False)
    record = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    task = db.relationship('Task', backref='result', lazy='dynamic')

    def __repr__(self):
        return '<task result file: {}>'.format(self.name)


class TaskLogFile(db.Model):
    __tablename__ = 't_task_logs'
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(128), nullable=False)

    task = db.relationship('Task', backref='log', lazy='dynamic')


task_database_data_association_table = db.Table('t_mapping__task_database_data',
                                                db.Column('database_data_id', db.Integer,
                                                          db.ForeignKey('t_database_datas.id')),
                                                db.Column('task_id', db.Integer, db.ForeignKey('t_tasks.id'))
                                                )

task_picture_catalog_association_table = db.Table('t_mapping__task_picture_catalog',
                                                  db.Column('picture_catalog_id', db.Integer,
                                                            db.ForeignKey('t_picture_catalogs.id')),
                                                  db.Column('task_id', db.Integer, db.ForeignKey('t_tasks.id'))
                                                  )

task_ds_data_link_association_table = db.Table('t_mapping__task_ds_data_link',
                                               db.Column('ds_data_link_id', db.Integer,
                                                         db.ForeignKey('t_data_source_data_links.id')),
                                               db.Column('task_id', db.Integer, db.ForeignKey('t_tasks.id'))
                                               )

task_data_excel_association_table = db.Table('t_mapping__task_data_excel',
                                             db.Column('excel_data_id', db.Integer,
                                                       db.ForeignKey('t_data_source_excel_sheets.id')),
                                             db.Column('task_id', db.Integer, db.ForeignKey('t_tasks.id'))
                                             )


class Task(db.Model):
    __tablename__ = 't_tasks'
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    run_time = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(120), default='')
    name = db.Column(db.String(50), nullable=False)

    # 外键
    status_id = db.Column(db.Integer, db.ForeignKey('t_task_status.id'), default=1)
    application_id = db.Column(db.Integer, db.ForeignKey('t_applications.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))
    result_file_id = db.Column(db.Integer, db.ForeignKey('t_task_results.id'))
    log_file_id = db.Column(db.Integer, db.ForeignKey('t_task_logs.id'))
    task_type_id = db.Column(db.Integer, db.ForeignKey('t_task_types.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('t_models.id'))

    database_data = db.relationship('DatabaseData', secondary=task_database_data_association_table,
                                    backref=db.backref('tasks', lazy='dynamic'), lazy='dynamic')
    picture_catalog = db.relationship('PictureCatalog', secondary=task_picture_catalog_association_table,
                                      backref=db.backref('tasks', lazy='dynamic'), lazy='dynamic')
    ds_data_link = db.relationship('DataSourceDataLink', secondary=task_ds_data_link_association_table,
                                   backref=db.backref('tasks', lazy='dynamic'), lazy='dynamic')
    data_excel = db.relationship('DataSourceExcelSheet', secondary=task_data_excel_association_table,
                                 backref=db.backref('tasks', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<task {} of application: {}>'.format(self.name, self.application.name)

    @property
    def predicted_data_link(self):
        if 1 == self.task_type_id:
            return self.data_excel.first()
        elif 2 == self.task_type_id:
            return self.picture_catalog.first()
        elif 3 == self.task_type_id:
            return self.database_data.first()
        elif 4 == self.task_type_id:
            return self.ds_data_link.first()
        else:
            raise TypeError('没有对应的任务类型')

    @property
    def model_name(self):
        return self.model.name
