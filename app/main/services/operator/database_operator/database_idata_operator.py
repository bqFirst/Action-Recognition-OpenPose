#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/3 16:25
# @Author : wangweimin
# @File   : database_idata_operator.py
# @Desc   :

import pandas as pd

from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.core.database.database_pool.database_pool import DatabasePool
from app.main.services.core.database.databases_connect_operator import DatabasesOperator
from app.main.basic_main.custom_error import DatabaseSelectError
from app.main.services.operator.base_common.data_base_operator.data_cale import get_data_link_record
from app.main.services.operator.base_common.data_base_operator.data_overview_operator import DataOverviewService
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.models import Database, DatabaseData


class DatabaseDataService(object):

    @staticmethod
    def select_data(database_id: int, sql: str, creator_id: int) -> pd.DataFrame:
        data = DatabaseSQLService.select(database_id=database_id, sql=sql, creator_id=creator_id)
        return data

    @classmethod
    def info(cls, data_link_id: int):
        database_data: DatabaseData = ObjectAcquisition.database_data(database_data_id=data_link_id)
        return {'data_name': database_data.name, 'database_id': database_data.database_id,
                'database_name': database_data.database.show_name(), 'sql': database_data.sql}

    @classmethod
    def get(cls, data_link_id: int, page: int, limit: int):
        database_data: DatabaseData = ObjectAcquisition.database_data(database_data_id=data_link_id)
        data = DataFileOperator(address='database').get(filename=database_data.alias,
                                                        paging={'start': page * limit, 'nrows': limit})
        return data, get_data_link_record(database_data)

    @classmethod
    def overview(cls, data_link_id):
        database_data: DatabaseData = ObjectAcquisition.database_data(database_data_id=data_link_id)
        return DataOverviewService.get(data_link=database_data)


class DatabaseSQLService(object):

    @staticmethod
    def __check_select_sql(sql: str):
        sql_lower: str = sql.lower()
        if not sql_lower.startswith('select'):
            raise DatabaseSelectError(ErrorMsg.get_error_message(20))
        if 'from' not in sql_lower:
            raise DatabaseSelectError(ErrorMsg.get_error_message(20))
        return

    @classmethod
    def select(cls, database_id: int, sql: str, creator_id: int) -> pd.DataFrame:
        cls.__check_select_sql(sql=sql)
        database: Database = ObjectAcquisition.database(database_id=database_id, creator_id=creator_id)
        pool: DatabasePool = DatabasesOperator.create_pool(database=database)
        try:
            data = pool.select(sql=sql)
        except Exception as e:
            raise DatabaseSelectError(str(e))
        return data
