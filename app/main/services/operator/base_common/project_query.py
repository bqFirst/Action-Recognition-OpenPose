#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/22 17:59
# @Author : wangweimin
# @File   : project_query.py
# @Desc   :

from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.models import Project, PictureCatalog, DataSourceDataLink, DataSourceExcelSheet, DatabaseData


def get_project_data_name_list(project_id: int) -> list:
    project: Project = ObjectAcquisition.project_by_id(project_id=project_id)
    result = []
    excel_data_list = project.excel_data.with_entities(DataSourceExcelSheet.name).all()
    result.extend([x[0] for x in excel_data_list])

    data_link_list = project.data_links.filter(DataSourceDataLink.data_type_id != 2).with_entities(
        DataSourceDataLink.name).all()
    result.extend([x[0] for x in data_link_list])

    picture_catalog_list = project.picture_catalogs.with_entities(PictureCatalog.name).all()
    result.extend([x[0] for x in picture_catalog_list])

    database_data_list = project.database_data.with_entities(DatabaseData.name).all()
    result.extend([x[0] for x in database_data_list])

    return result
