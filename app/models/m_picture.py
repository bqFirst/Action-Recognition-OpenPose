#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/12 11:14
# @Author : wangweimin
# @File   : m_picture.py
# @Desc   :

from app import db
from datetime import datetime

picture_catalog_project_association_table = db.Table('t_mapping__picture_catalog_project',
                                                     db.Column('picture_catalog_id', db.Integer,
                                                               db.ForeignKey('t_picture_catalogs.id')),
                                                     db.Column('project_id', db.Integer, db.ForeignKey('t_projects.id'))
                                                     )


class PictureCatalog(db.Model):
    __tablename__ = 't_picture_catalogs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    record = db.Column(db.Integer)

    # 外键
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))

    pictures = db.relationship('Picture', backref='picture_catalog', lazy='dynamic')
    labels = db.relationship('PictureLabel', backref='picture_catalog', lazy='dynamic')

    projects = db.relationship('Project', secondary=picture_catalog_project_association_table,
                               backref=db.backref('picture_catalogs', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<picture catalog: {}>'.format(self.name)

    @property
    def application(self):
        return self.applications.first()

    @property
    def type(self):
        return 'picture'


class Picture(db.Model):
    __tablename__ = 't_pictures'
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    size = db.Column(db.Integer)
    is_used = db.Column(db.Boolean, default=False)

    # 外键
    picture_catalog_id = db.Column(db.Integer, db.ForeignKey('t_picture_catalogs.id'))
    thumbnail_id = db.Column(db.Integer, db.ForeignKey('t_thumbnails.id'))

    def __repr__(self):
        return '<picture: {}>'.format(self.name)

    @property
    def label(self) -> list:
        labels: list = self.labels.all()
        try:
            return [label.name for label in labels]
        except TypeError:
            return []

    @property
    def label_num(self) -> int:
        return self.labels.count()


picture_label_picture_association_table = db.Table('t_mapping__picture_label_picture',
                                                   db.Column('picture_label_id', db.Integer,
                                                             db.ForeignKey('t_picture_labels.id')),
                                                   db.Column('picture_id', db.Integer, db.ForeignKey('t_pictures.id'))
                                                   )


class PictureLabel(db.Model):
    __tablename__ = 't_picture_labels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)

    # 外键
    picture_catalog_id = db.Column(db.Integer, db.ForeignKey('t_picture_catalogs.id'))

    pictures = db.relationship('Picture', secondary=picture_label_picture_association_table,
                               backref=db.backref('labels', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<picture catalog: {}, label: {}>'.format(self.picture_catalog.name, self.name)


class Thumbnail(db.Model):
    __tablename__ = 't_thumbnails'
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(50), nullable=False)

    pictures = db.relationship('Picture', backref='thumbnail', lazy='dynamic')

    @property
    def picture(self):
        return self.pictures.first()

    def __repr__(self):
        return '<thumbnail of picture: {}>'.format(self.picture.name)
