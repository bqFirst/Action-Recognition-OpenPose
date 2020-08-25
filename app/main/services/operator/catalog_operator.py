#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/23 10:52
# @Author : wangweimin
# @File   : catalog_operator.py
# @Desc   :

from app.main.services.operator.base_common.data_base_operator.data_transform import datetime2timestamp
from app.models import DataSourceCatalog, DataSourceDataLink, Project, ProjectCatalog, Application, ApplicationCatalog


def data_source_tree(catalog_id: int) -> list:
    result = []
    for data_link in DataSourceDataLink.query.filter(DataSourceDataLink.catalog_id == catalog_id).all():
        data_type_id = data_link.data_type_id
        if 1 == data_type_id:
            data_msg = dict()
            data_msg['name'], data_msg['data_type'] = data_link.name, data_link.type
            data_msg['type'] = 'data'
            data_msg['data_link_id'] = data_link.id
            result.append(data_msg)
        else:
            for data_sheet in data_link.excel_sheets.all():
                data_msg = dict()
                data_msg['name'], data_msg['data_type'] = data_sheet.name, data_sheet.type
                data_msg['type'] = 'data'
                data_msg['data_link_id'] = data_sheet.id
                result.append(data_msg)
    data_source_catalogs: list = DataSourceCatalog.query.filter(DataSourceCatalog.pid == catalog_id).all()
    for data_source_catalog in data_source_catalogs:
        catalog_menu = dict()
        catalog_menu['name'] = data_source_catalog.name
        catalog_menu['type'] = 'catalog'
        catalog_menu['catalog_id'] = data_source_catalog.id
        catalog_menu['child'] = data_source_tree(catalog_id=data_source_catalog.id)
        result.append(catalog_menu)
    return result


def data_source_data_links():
    data_links: list = DataSourceDataLink.query.all()
    result = []
    for data_link in data_links:
        data_msg = dict()
        data_msg['creator'] = data_link.creator.name
        data_msg['data_id'] = data_link.id
        data_msg['create_time'] = data_link.create_time
        data_msg['data_name'] = data_link.name
        data_msg['data_type'] = data_link.data_type.data_type
        result.append(data_msg)
    return result


def project_tree(catalog_id: int) -> list:
    result = []
    for project in Project.query.filter(Project.catalog_id == catalog_id).all():
        project_msg = dict()
        project_msg['type'] = 'project'
        project_msg['name'] = project.name
        project_msg['project_id'] = project.id
        result.append(project_msg)
    project_catalogs: list = ProjectCatalog.query.filter(ProjectCatalog.pid == catalog_id).all()
    for project_catalog in project_catalogs:
        catalog_menu = dict()
        catalog_menu['name'] = project_catalog.name
        catalog_menu['type'] = 'catalog'
        catalog_menu['catalog_id'] = project_catalog.id
        catalog_menu['child'] = project_tree(catalog_id=project_catalog.id)
        catalog_menu['create_time'] = datetime2timestamp(project_catalog.create_time)
        result.append(catalog_menu)
    return result


def application_tree(catalog_id: int) -> list:
    result = []
    for application in Application.query.filter(Application.catalog_id == catalog_id).all():
        project_msg = dict()
        project_msg['type'] = 'application'
        project_msg['name'] = application.name
        project_msg['application_id'] = application.id
        result.append(project_msg)
    application_catalogs: list = ApplicationCatalog.query.filter(ApplicationCatalog.pid == catalog_id).all()
    for application_catalog in application_catalogs:
        catalog_menu = dict()
        catalog_menu['name'] = application_catalog.name
        catalog_menu['type'] = 'catalog'
        catalog_menu['catalog_id'] = application_catalog.id
        catalog_menu['child'] = application_tree(catalog_id=application_catalog.id)
        result.append(catalog_menu)
    return result
