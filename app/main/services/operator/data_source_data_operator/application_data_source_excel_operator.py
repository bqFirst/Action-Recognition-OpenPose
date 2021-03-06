#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/29 10:21
# @Author : wangwei
# @File   : application_data_source_excel_operator.py
# @Desc   :

import os
import pandas as pd

from app import db

from app.main.basic_main.custom_error import UserOperatorError, RequestValueError, RequestIdError, NameRepeatedError
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.data_base_operator.data_overview_operator import DataOverviewService
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.data_source_data_operator.data_source_iexcel_operator import DsExcelService, \
    DsExcelCache
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectExistJudgement, \
    ObjectNameRepeatedJudgement
from conf.data_path import DataDirectoryPath
from app.models import DataSourceDataLink, DataOverview, DataSourceExcelSheet, Application, DataType, Task


class AppDsExcelService(DsExcelService):

    @classmethod
    def upload_put(
            cls,
            data_name_map: dict,
            catalog_id: int,
            user_id: int,
            application_id: int,
            uuid_: str,
            data_type: str) -> list:
        cache = DsExcelCache.get(uuid_=uuid_)
        data = cache.get('data')
        filename: str = cache.get('filename')
        application: Application = ObjectAcquisition.application_by_id(
            application_id=application_id)
        ObjectExistJudgement.ds_catalog_id(catalog_id=catalog_id)
        sheet_names: list = data.sheet_names
        new_sheet_names = list(data_name_map.values())
        if len(set(new_sheet_names)) != len(new_sheet_names):
            raise RequestValueError(ErrorMsg.get_error_message(28))
        for old_sheet_name, new_sheet_name in data_name_map.items():
            if old_sheet_name not in sheet_names:
                raise RequestValueError(ErrorMsg.get_error_message(22))
            try:
                ObjectNameRepeatedJudgement.application_data_by_application_id(
                    data_name=new_sheet_name, application_id=application_id)
            except NameRepeatedError:
                raise NameRepeatedError(ErrorMsg.get_error_message(57).format(new_sheet_name))
        data_type: DataType = ObjectAcquisition.data_type_by_name(
            data_type=data_type)
        alias = ''
        data_link = DataSourceDataLink(
            name=filename,
            alias=alias,
            data_type=data_type,
            creator_id=user_id,
            catalog_id=catalog_id)
        db.session.add(data_link)
        db.session.commit()
        data_link.applications.append(application)
        db.session.commit()
        data_operator = DataFileOperator(address='data_source')
        data_link_id = []
        for old_sheet_name, new_sheet_name in data_name_map.items():
            sheet_data = data.parse(old_sheet_name)
            sheet_alias: str = get_uuid_name(suffix='csv')
            data_operator.put(data=sheet_data, file_name=sheet_alias)
            data_excel: DataSourceExcelSheet = DataSourceExcelSheet(
                name=new_sheet_name,
                alias=sheet_alias,
                data_link=data_link,
                record=sheet_data.shape[0])
            db.session.add(data_excel)
            db.session.commit()
            data_excel.applications.append(application)
            db.session.commit()
            data_link_id.append(data_excel.id)
        return data_link_id

    @classmethod
    def rename(
            cls,
            data_link_id: int,
            catalog_id: int,
            new_name: str,
            application_id: int = None):
        data_link: DataSourceExcelSheet = ObjectAcquisition.ds_excel(
            data_excel_id=data_link_id, ascription='application')
        if application_id is not None and application_id != data_link.application.id:
            raise RequestIdError(ErrorMsg.get_error_message(27))
        else:
            application_id = data_link.application.id

        if data_link.name == new_name:
            return
        if new_name is not None:
            ObjectNameRepeatedJudgement.application_data_by_application_id(
                data_name=new_name, application_id=application_id)
            data_link.name = new_name

        db.session.commit()

    @classmethod
    def delete(cls, data_link_id: int, is_forced=False) -> bool:
        data_sheet: DataSourceExcelSheet = ObjectAcquisition.ds_excel(
            data_excel_id=data_link_id, ascription='application')
        if not is_forced:
            task_list = data_sheet.tasks.with_entities(Task.name).all()
            if len(task_list) > 0:
                task_name_list = [x[0] for x in task_list]
                raise UserOperatorError(
                    ErrorMsg.get_error_message(31).format(
                        ','.join(task_name_list)))
        DataOverviewService.delete(data_link=data_sheet)
        data_link: DataSourceDataLink = data_sheet.data_link
        DataFileOperator(
            address='data_source').delete(
            file_name=data_sheet.alias)
        db.session.delete(data_sheet)
        db.session.commit()
        if not data_link.excel_sheets.all():
            db.session.delete(data_link)
            db.session.commit()
        return True


def ds_excel_create_service(
        data_link: DataSourceDataLink,
        application_id: int):
    alias: str = data_link.alias
    name: str = data_link.name
    file: str = os.path.join(DataDirectoryPath.get_data_source_path(), alias)
    reader = pd.ExcelFile(file)
    sheet_names: list = reader.sheet_names
    for sheet_name in sheet_names:
        data = reader.parse(sheet_name)
        sheet_alias: str = get_uuid_name(suffix='csv')
        DataFileOperator(
            address='data_source').put(
            data=data,
            file_name=sheet_alias)
        data_excel: DataSourceExcelSheet = DataSourceExcelSheet(
            name=name + '-' + sheet_name,
            alias=sheet_alias,
            data_link=data_link,
            application_id=application_id,
            record=data.shape[0])
        db.session.add(data_excel)
        db.session.commit()


def delete_sheet_data(data_sheet: DataSourceExcelSheet) -> bool:
    data_overview: DataOverview = data_sheet.data_overview
    if data_overview is not None:
        DataFileOperator(
            address='overview').delete(
            file_name=data_overview.alias)
        db.session.delete(data_overview)
        db.session.commit()
    data_link: DataSourceDataLink = data_sheet.data_link
    DataFileOperator(address='data_source').delete(file_name=data_sheet.alias)
    db.session.delete(data_sheet)
    db.session.commit()
    if not data_link.excel_sheets.all():
        DataFileOperator(
            address='data_source').delete(
            file_name=data_link.alias)
        db.session.delete(data_link)
        db.session.commit()
    return True
