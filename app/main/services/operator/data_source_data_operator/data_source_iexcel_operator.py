#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/3 16:15
# @Author : wangweimin
# @File   : data_source_iexcel_operator.py
# @Desc   :

import pandas as pd

from expiringdict import ExpiringDict
from werkzeug.datastructures import FileStorage

from app.main.basic_main.custom_error import UserOperatorError, DataParsingError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.data_base_operator.data_cale import get_data_link_record
from app.main.services.operator.base_common.data_base_operator.data_overview_operator import DataOverviewService
from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.models import DataSourceExcelSheet


class DsExcelCache(object):
    Cache = ExpiringDict(max_age_seconds=1 * 60 * 60, max_len=100)  # {'uuid': {'data': data, 'filename': name}}

    @classmethod
    def put(cls, uuid_: str, data: dict):
        if len(cls.Cache) == cls.Cache.max_len:
            raise UserOperatorError(ErrorMsg.get_error_message(25))
        cls.Cache[uuid_] = data

    @classmethod
    def get(cls, uuid_: str) -> dict:
        try:
            return cls.Cache[uuid_]
        except KeyError:
            raise UserOperatorError(ErrorMsg.get_error_message(error_id=21))

    @classmethod
    def delete(cls, uuid_: str):
        cls.Cache.pop(uuid_)


class DsExcelService(object):

    @classmethod
    def upload_delete(cls, uuid_: str):
        DsExcelCache.delete(uuid_=uuid_)

    @staticmethod
    def parsing(f: FileStorage):
        try:
            data = pd.ExcelFile(f)
            return data
        except Exception:
            raise DataParsingError(ErrorMsg.get_error_message(29))

    @classmethod
    def upload_post(cls, f):
        cls.check_excel(f=f)
        data = cls.parsing(f)
        filename = f.filename
        uuid_ = get_uuid_name()
        DsExcelCache.put(uuid_=uuid_, data={'data': data, 'filename': filename})
        return {'uuid': uuid_, 'sheet_names': data.sheet_names}

    @staticmethod
    def allowed_file(filename: str):
        return '.' in filename and filename.rsplit('.', 1)[1] in ['xls', 'xlsx']

    @classmethod
    def check_excel(cls, f):
        if f and cls.allowed_file(f.filename):
            pass
        else:
            raise UserOperatorError(ErrorMsg.get_error_message(68))

    @classmethod
    def overview(cls, data_link_id: int) -> list:
        data_link: DataSourceExcelSheet = ObjectAcquisition.ds_excel(data_excel_id=data_link_id)
        return DataOverviewService.get(data_link=data_link)

    @classmethod
    def get(cls, data_link_id: int, page: int, limit: int):
        data_link: DataSourceExcelSheet = ObjectAcquisition.ds_excel(data_excel_id=data_link_id)
        data = DataFileOperator(address='data_source').get(filename=data_link.alias,
                                                           paging={'start': page * limit, 'nrows': limit})
        return data, get_data_link_record(data_link)
