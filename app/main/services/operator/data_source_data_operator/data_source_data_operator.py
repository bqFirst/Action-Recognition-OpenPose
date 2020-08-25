#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/19 9:53
# @Author : wangweimin
# @File   : data_source_data_operator.py
# @Desc   :

import os
import pandas as pd

from app import db
from app.models import DataSourceDataLink, DataOverview, DataSourceExcelSheet, Project, DataType
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.basic_main.custom_error import UserOperatorError
from app.main.services.operator.base_common.file_operator import file_write_service
from app.main.services.operator.base_common.data_base_operator.data_cale import get_data_link_record
from app.main.services.operator.base_common.data_base_operator.data_overview_operator import DataOverviewService
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectExistJudgement, \
    ObjectNameRepeatedJudgement
from conf.data_path import DataDirectoryPath


class DsDataLinkService(object):

    @staticmethod
    def __allowed_execl_file(filename: str):
        return '.' in filename and filename.rsplit('.', 1)[1] in ['xls', 'xlsx', 'csv']

    @classmethod
    def upload(cls, f, data_name: str, catalog_id: int, user_id: int, data_type: str, project_id: int):
        project: Project = ObjectAcquisition.project_by_id(project_id=project_id)
        ObjectExistJudgement.ds_catalog_id(catalog_id=catalog_id)
        ObjectNameRepeatedJudgement.project_data_by_project_id(data_name=data_name, project_id=project_id)
        data_type: DataType = ObjectAcquisition.data_type_by_name(data_type=data_type)
        if f and cls.__allowed_execl_file(f.filename):
            alias = file_write_service(f=f, address='data_source')
            data_link = DataSourceDataLink(name=data_name, alias=alias, data_type=data_type, creator_id=user_id,
                                           catalog_id=catalog_id)
            db.session.add(data_link)
            db.session.commit()
            data_link.projects.add(project)
            db.session.commit()
        else:
            raise UserOperatorError('Unsuccessfully obtained file or format is not allowed')
        if 'csv' == data_type.data_type:
            pass
        elif 'excel' == data_type.data_type:
            ds_excel_create_service(data_link=data_link, project_id=project_id)
        else:
            pass

    @classmethod
    def rename(cls, data_link_id: int, catalog_id: int, new_name: str, data_type: str):
        if 'csv' == data_type:
            data_link: DataSourceDataLink = ObjectAcquisition.ds_data_link(data_link_id=data_link_id)
            project_id = data_link.projects.first().id
        elif 'excel' == data_type:
            data_link: DataSourceExcelSheet = ObjectAcquisition.ds_excel(data_excel_id=data_link_id)
            project_id = data_link.project_id
        else:
            data_link = None
            project_id = None
            # raise ValueError('Not exists data type {}'.format(data_type))
        if new_name is None:
            new_name: str = data_link.name
        ObjectNameRepeatedJudgement.project_data_by_project_id(data_name=new_name, project_id=project_id)
        # if catalog_id is None:
        #     catalog_id: int = data_link.catalog_id
        data_link.name = new_name
        # data_link.catalog_id = catalog_id
        db.session.commit()

    @classmethod
    def delete(cls, data_link_id: int, data_type: str, is_forced=False) -> bool:
        if 'excel' == data_type:
            return ds_data_link_sheet_delete_service(data_sheet_id=data_link_id, is_forced=is_forced)

        # 非excel文件删除
        data_link: DataSourceDataLink = ObjectAcquisition.ds_data_link(data_link_id=data_link_id)
        if data_link.is_used and not is_forced:
            return False
        cls.__delete_data_link(data_link=data_link)
        return True

    @classmethod
    def overview(cls, data_link_id: int, data_type: str) -> list:
        data_link = cls.__get_data_link(data_link_id=data_link_id, data_type=data_type)
        return DataOverviewService.get(data_link=data_link)

    @classmethod
    def get(cls, data_link_id: int, data_type: str, page: int, limit: int):
        data_link = cls.__get_data_link(data_link_id=data_link_id, data_type=data_type)
        data = DataFileOperator(address='data_source').get(filename=data_link.alias,
                                                           paging={'start': page * limit, 'nrows': limit})
        return data, get_data_link_record(data_link)

    @staticmethod
    def __get_data_link(data_link_id: int, data_type: str):
        if 'excel' == data_type:
            data_link: DataSourceExcelSheet = ObjectAcquisition.ds_excel(data_excel_id=data_link_id)
        else:
            data_link: DataSourceDataLink = ObjectAcquisition.ds_data_link_by_type(data_link_id=data_link_id,
                                                                                   data_type=data_type)
        return data_link

    @staticmethod
    def __delete_data_link(data_link: DataSourceDataLink) -> None:
        projects: list = data_link.projects.all()
        if projects is None:
            pass
        else:
            for project in projects:
                data_link.projects.remove(project)
            db.session.commit()
        alias = data_link.alias
        DataFileOperator(address='data_source').delete(file_name=alias)
        DataOverviewService.delete(data_link=data_link)
        db.session.delete(data_link)
        db.session.commit()


# def delete_sheet_data(data_link: DataSourceDataLink, sheet_name: str) -> None:
#     alias: str = data_link.alias
#     if alias.endswith(('xlsx', 'xls', 'excel')):
#         file = os.path.join(DataDirectoryPath.get_data_source_path(), alias)
#         reader = pd.ExcelFile(file)
#         sheet_names: list = reader.sheet_names
#         if 1 == len(sheet_names):
#             # 若文件被引用，无法删除，数据库自动识别，无法删除
#             delete_data_link(data_link=data_link)
#             DataFileOperator(address='data_source').delete(file_name=alias)
#         else:
#             wb = openpyxl.load_workbook(file)
#             ws = wb[sheet_name]
#             wb.remove(ws)
#             wb.save(file)
#     elif alias.endswith('csv'):
#         delete_data_link(data_link=data_link)
#         DataFileOperator(address='data_source').delete(file_name=alias)
#     else:
#         delete_data_link(data_link=data_link)
#         DataFileOperator(address='data_source').delete(file_name=alias)

def ds_excel_create_service(data_link: DataSourceDataLink, project_id: int):
    alias: str = data_link.alias
    name: str = data_link.name
    file: str = os.path.join(DataDirectoryPath.get_data_source_path(), alias)
    reader = pd.ExcelFile(file)
    sheet_names: list = reader.sheet_names  # 页签名
    for sheet_name in sheet_names:
        data = reader.parse(sheet_name)
        sheet_alias: str = get_uuid_name(suffix='csv')
        DataFileOperator(address='data_source').put(data=data, file_name=sheet_alias)
        data_excel: DataSourceExcelSheet = DataSourceExcelSheet(name=name + '-' + sheet_name, alias=sheet_alias,
                                                                data_link=data_link, project_id=project_id,
                                                                record=data.shape[0])
        db.session.add(data_excel)
        db.session.commit()


def delete_sheet_data(data_sheet: DataSourceExcelSheet) -> bool:
    data_overview: DataOverview = data_sheet.data_overview
    if data_overview is not None:
        DataFileOperator(address='overview').delete(file_name=data_overview.alias)
        db.session.delete(data_overview)
        db.session.commit()
    data_link: DataSourceDataLink = data_sheet.data_link
    DataFileOperator(address='data_source').delete(file_name=data_sheet.alias)
    db.session.delete(data_sheet)
    db.session.commit()
    if not data_link.excel_sheets.all():
        DataFileOperator(address='data_source').delete(file_name=data_link.alias)
        db.session.delete(data_link)
        db.session.commit()
    return True


def ds_data_link_sheet_delete_service(data_sheet_id: int, is_forced=False) -> bool:
    data_sheet: DataSourceExcelSheet = ObjectAcquisition.ds_excel(data_excel_id=data_sheet_id)
    if data_sheet.is_used and not is_forced:
        return False
    return delete_sheet_data(data_sheet=data_sheet)
