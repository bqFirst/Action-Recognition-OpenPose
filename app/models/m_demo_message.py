#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/3/2 10:13
# @Author : wangweimin
# @File   : m_demo_message.py
# @Desc   :
"""
案例demo数据
"""

from app import db


class City(db.Model):
    __tablename__ = 't_cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)

    districts = db.relationship('UrbanDistrict', backref='city', lazy='dynamic')


class UrbanDistrict(db.Model):
    __tablename__ = 't_districts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)

    # 外键
    city_id = db.Column(db.Integer, db.ForeignKey('t_cities.id'))

    street = db.relationship('CameraDistribution', backref='district', lazy='dynamic')

    def __repr__(self):
        return f'{self.full_name}'

    @property
    def full_name(self):
        return self.city.name + self.name


class CameraDistribution(db.Model):
    __tablename__ = 't_camera_distributions'
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Integer)

    # 外键
    district_id = db.Column(db.Integer, db.ForeignKey('t_districts.id'))

    def __repr__(self):
        return f'<{self.longitude},{self.latitude}>{self.address}'

    @property
    def district(self):
        return self.district.full_name


class CameraBusiness(db.Model):
    __tablename__ = 't_camera_businesses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'{self.name}({self.telephone})'


class CameraType(db.Model):
    __tablename__ = 't_camera_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'{self.name}'
