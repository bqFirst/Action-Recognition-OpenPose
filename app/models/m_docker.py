#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/31 9:08
# @Author : wangweimin
# @File   : m_docker.py
# @Desc   :

from app import db


class DockerImageFile(db.Model):
    __tablename__ = 't_image_files'
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(128), default='')

    # 外键
    status_id = db.Column(db.Integer, db.ForeignKey('t_docker_image_status.id'), default=1)

    applications = db.relationship('Application', backref='application_image', lazy='dynamic')

    def __repr__(self):
        return '<image file of application {}>'.format(self.applications.first().name)

    @property
    def status(self):
        return self.image_status


class DockerImage(db.Model):
    __tablename__ = 't_docker_images'
    id = db.Column(db.Integer, primary_key=True)
    tags = db.Column(db.String(128), nullable=False, unique=True)
    short_id = db.Column(db.String(18), nullable=False)
    alias = db.Column(db.String(128), default='')  # 迟早删掉

    # 外键
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('t_docker_image_status.id'), default=1)

    containers = db.relationship('DockerContainer', backref='image', lazy='dynamic')
    images = db.relationship('ModelVersion', backref='image', lazy='dynamic')  # 命名失误

    def __repr__(self):
        return '<docker image: {}>'.format(self.tags)

    @property
    def status(self):
        return self.image_status


class DockerPort(db.Model):
    __tablename__ = 't_docker_ports'
    id = db.Column(db.Integer, primary_key=True)
    port = db.Column(db.Integer, nullable=False, unique=True)

    docker_containers = db.relationship('DockerContainer', backref='docker_port', lazy='dynamic')
    case_docker_containers = db.relationship('CaseDockerContainer', backref='docker_port', lazy='dynamic')

    def __repr__(self):
        return '<docker port: {}>'.format(self.port)


class DockerContainer(db.Model):
    __tablename__ = 't_docker_containers'
    id = db.Column(db.Integer, primary_key=True)
    short_id = db.Column(db.String(18), nullable=False)
    alias = db.Column(db.String(128), nullable=False)  # 数据目录

    # 外键
    creator_id = db.Column(db.Integer, db.ForeignKey('t_users.id'))
    image_id = db.Column(db.Integer, db.ForeignKey('t_docker_images.id'))
    base_image_id = db.Column(db.Integer, db.ForeignKey('t_docker_base_images.id'))
    docker_port_id = db.Column(db.Integer, db.ForeignKey('t_docker_ports.id'))

    application = db.relationship('Application', backref='container', lazy='dynamic')

    def __repr__(self):
        return '<docker container: {}>'.format(self.name)

    @property
    def port(self):
        return self.docker_port.port


class CaseDockerContainer(db.Model):
    __tablename__ = 't_case_docker_containers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)  # 描述容器内提供的服务
    short_id = db.Column(db.String(18), nullable=False)

    # 外键
    docker_port_id = db.Column(db.Integer, db.ForeignKey('t_docker_ports.id'))

    case = db.relationship('Case', backref='container', lazy='dynamic')  # 案例容器具备
    model_assessment = db.relationship('DockerModelAssessment', backref='container', lazy='dynamic')  # 案例容器具备
    model_mode = db.relationship('DockerModelMode', backref='container', lazy='dynamic')  # 案例容器具备

    def __repr__(self):
        return '<docker container: {}>'.format(self.name)

    @property
    def port(self):
        return self.docker_port.port


class DockerModelAssessment(db.Model):
    __tablename__ = 't_docker_model_assessments'
    id = db.Column(db.Integer, primary_key=True)
    attribute = db.Column(db.String(128), nullable=False)
    value = db.Column(db.String(128), nullable=False)

    # 外键
    container_id = db.Column(db.Integer, db.ForeignKey('t_case_docker_containers.id'))

    def __repr__(self):
        return '<assessment of case: {}>'.format(self.cases.first().name)


class DockerModelMode(db.Model):
    __tablename__ = 't_docker_model_modes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    # 外键
    container_id = db.Column(db.Integer, db.ForeignKey('t_case_docker_containers.id'))

    input_params = db.relationship('InputParam', backref='mode', lazy='dynamic')
    output_params = db.relationship('OutputParam', backref='mode', lazy='dynamic')

    def __repr__(self):
        return '<model mode {} of docker container: {}>'.format(self.name, self.container.name)


class InputParam(db.Model):
    __tablename__ = 't_input_params'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    required = db.Column(db.Boolean, nullable=False, default=False)

    # 外键
    mode_id = db.Column(db.Integer, db.ForeignKey('t_docker_model_modes.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('t_param_types.id'))

    def __repr__(self):
        mode = self.mode
        return '<input param {} of mode {} of docker container: {}>'.format(self.name, mode.name, mode.container.name)


class OutputParam(db.Model):
    __tablename__ = 't_output_params'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(50), nullable=False)

    # 外键
    mode_id = db.Column(db.Integer, db.ForeignKey('t_docker_model_modes.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('t_param_types.id'))

    def __repr__(self):
        mode = self.mode
        return '<output param {} of mode {} of docker container: {}>'.format(self.name, mode.name, mode.container.name)
