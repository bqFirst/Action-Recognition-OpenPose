#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/29 15:40
# @Author : wangwei
# @File   : appication_query.py
# @Desc   : 

from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.models import Application, PictureCatalog, DataSourceDataLink, DataSourceExcelSheet, DatabaseData


def get_application_data_name_list(application_id: int) -> list:
    application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
    result = []
    excel_data_list = application.excel_data.with_entities(DataSourceExcelSheet.name).all()
    result.extend([x[0] for x in excel_data_list])

    data_link_list = application.data_links.filter(DataSourceDataLink.data_type_id != 2).with_entities(
        DataSourceDataLink.name).all()
    result.extend([x[0] for x in data_link_list])

    picture_catalog_list = application.picture_catalogs.with_entities(PictureCatalog.name).all()
    result.extend([x[0] for x in picture_catalog_list])

    database_data_list = application.database_data.with_entities(DatabaseData.name).all()
    result.extend([x[0] for x in database_data_list])

    return result
