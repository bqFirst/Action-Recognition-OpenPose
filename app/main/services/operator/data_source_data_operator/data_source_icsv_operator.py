#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/3 16:05
# @Author : wangweimin
# @File   : data_source_icsv_operator.py
# @Desc   :

import os
import pandas as pd
from werkzeug.datastructures import FileStorage

from app.models import DataSourceDataLink
from app.main.basic_main.custom_error import DataParsingError, UserOperatorError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.data_base_operator.data_cale import get_data_link_record
from app.main.services.operator.base_common.data_base_operator.data_overview_operator import DataOverviewService
from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from conf.data_path import DataDirectoryPath


class DsCsvService(object):

    @staticmethod
    def parsing(f: FileStorage) -> pd.DataFrame:
        alias: str = get_uuid_name(suffix='csv')
        file = os.path.join(DataDirectoryPath.get_temp_path(), alias)
        f.save(file)
        # noinspection PyBroadException
        try:
            data = pd.read_csv(file, encoding='gbk')
        except Exception:
            try:
                data = pd.read_csv(file)
            except Exception:
                raise DataParsingError(ErrorMsg.get_error_message(29))
            finally:
                DataDirectoryPath.rm_file(file=file)
        finally:
            DataDirectoryPath.rm_file(file=file)
        return data

    @staticmethod
    def allowed_file(filename: str):
        return '.' in filename and filename.rsplit('.', 1)[1] in ['csv']

    @classmethod
    def check_csv(cls, f):
        if f and cls.allowed_file(f.filename):
            pass
        else:
            raise UserOperatorError(ErrorMsg.get_error_message(68))

    @classmethod
    def overview(cls, data_link_id: int) -> list:
        data_link: DataSourceDataLink = ObjectAcquisition.ds_data_link(data_link_id=data_link_id)
        return DataOverviewService.get(data_link=data_link)

    @classmethod
    def get(cls, data_link_id: int, page: int, limit: int):
        data_link: DataSourceDataLink = ObjectAcquisition.ds_data_link(data_link_id=data_link_id)
        data = DataFileOperator(address='data_source').get(filename=data_link.alias,
                                                           paging={'start': page * limit, 'nrows': limit})
        return data, get_data_link_record(data_link)
