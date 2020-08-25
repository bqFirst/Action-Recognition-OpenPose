#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/17 11:12
# @Author : wangweimin
# @File   : project_path.py
# @Desc   :

import os

from sqlalchemy import and_

from app.main.basic_main.custom_error import RequestValueError
from app.models import ProjectCatalog, Project


def get_project_id_by_path(project_path: str) -> int:
        path_split: list = project_path.split(os.path.sep)
        if len(path_split) <= 1:
            raise RequestValueError('Error project path')
        catalog_name_list = path_split[:-1]
        project_name = path_split[-1]
        catalog_id = 0
        for catalog_name in catalog_name_list:
            catalog: ProjectCatalog = ProjectCatalog.query.filter(
                and_(ProjectCatalog.pid == catalog_id, ProjectCatalog.name == catalog_name)).first()
            if catalog is None:
                raise RequestValueError('Error catalog name: {}'.format(catalog_name))
            else:
                catalog_id = catalog.id
        project: Project = Project.query.filter(
            and_(Project.catalog_id == catalog_id, Project.name == project_name)).first()
        if project is None:
            raise RequestValueError('Error project name: {}'.format(project_name))
        else:
            return project.id


def get_project_path_by_id(project_id) -> str:
    path_list: list = []
    project: Project = Project.query.get(project_id)
    path_list.append(project.name)
    catalog: ProjectCatalog = project.catalog
    path_list.append(catalog.name)
    catalog_pid: int = catalog.pid
    while catalog_pid != 0:
        pcatalog: ProjectCatalog = ProjectCatalog.query.get(catalog_pid)
        path_list.append(pcatalog.name)
        catalog_pid = pcatalog.pid
    return os.path.sep.join(path_list[::-1])
