#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/24 9:50
# @Author : wangweimin
# @File   : project_src_data_operator.py
# @Desc   :

from app import db
from app.main.basic_main.custom_error import NameRepeatedError
from app.main.services.operator.base_common.data_base_operator.data_cale import get_data_link_record
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectNameRepeatedJudgement
from app.models import Project, PictureCatalog, DataSourceDataLink, DataSourceExcelSheet, DatabaseData


def get_picture_catalog_record(picture_catalog: PictureCatalog):
    record: int = picture_catalog.record
    if isinstance(record, int):
        return record
    record = picture_catalog.pictures.count()
    picture_catalog.record = record
    db.session.commit()
    return record


class ProjectSrcDataService(object):

    @classmethod
    def info(cls, project_id: int):
        project: Project = Project.query.get(project_id)
        result = []
        data_links = project.data_links.order_by(DataSourceDataLink.name).all()
        for data_link in data_links:
            data_type = data_link.type
            if 'excel' == data_type:
                for data_sheet in data_link.excel_sheets.order_by(DataSourceExcelSheet.name).all():
                    data_link_info = dict()
                    data_link_info['create_time'] = data_link.create_time
                    data_link_info['data_name'] = data_sheet.name
                    data_link_info['data_link_id'] = data_sheet.id
                    data_link_info['data_type'] = data_type
                    data_link_info['record'] = get_data_link_record(data_sheet)
                    result.append(data_link_info)
                continue
            data_link_info = dict()
            data_link_info['create_time'] = data_link.create_time
            data_link_info['data_name'] = data_link.name
            data_link_info['data_link_id'] = data_link.id
            data_link_info['data_type'] = data_type
            data_link_info['record'] = get_data_link_record(data_link)
            result.append(data_link_info)
        picture_catalogs = project.picture_catalogs.order_by(PictureCatalog.name).all()
        for picture_catalog in picture_catalogs:
            data_link_info = dict()
            data_link_info['create_time'] = picture_catalog.create_time
            data_link_info['data_name'] = picture_catalog.name
            data_link_info['data_link_id'] = picture_catalog.id
            data_link_info['data_type'] = 'picture'
            data_link_info['record'] = get_picture_catalog_record(picture_catalog)
            result.append(data_link_info)
        database_datas = project.database_data.order_by(DatabaseData.name).all()
        for database_data in database_datas:
            # from app.models import DatabaseData
            # database_data: DatabaseData = None
            data_link_info = dict()
            data_link_info['create_time'] = database_data.create_time
            data_link_info['data_name'] = database_data.name
            data_link_info['data_link_id'] = database_data.id
            data_link_info['data_type'] = database_data.type
            data_link_info['record'] = get_data_link_record(database_data)
            result.append(data_link_info)
        result = sorted(result, key=lambda x: x['data_type'])
        return result

    @classmethod
    def name_verify(cls, project_id: int, data_name: str) -> bool:
        try:
            ObjectNameRepeatedJudgement.project_data_by_project_id(data_name=data_name, project_id=project_id)
        except NameRepeatedError:
            return False
        return True
