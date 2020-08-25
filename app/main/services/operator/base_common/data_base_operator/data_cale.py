#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/19 10:02
# @Author : wangweimin
# @File   : data_cale.py
# @Desc   :

import pandas as pd

from app import db
from app.main.services.core.basic.uuid_name import get_uuid_name
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.models import DataSourceDataLink, DataOverview, DataSourceExcelSheet, ProjectProcessData, DatabaseData, TaskResultFile


def get_data_link_record(data_link) -> int:
    """

    :param data_link: ProjectProcessData Type or DataSourceExcelSheet Type or DataSourceDataLink Type or DatabaseData or TaskResultFile
    :return:
    """
    record: int = data_link.record
    if isinstance(record, int):
        return record
    alias: str = data_link.alias
    if isinstance(data_link, ProjectProcessData):
        data: pd.DataFrame = DataFileOperator(address='project').get(filename=alias)
    elif isinstance(data_link, DataSourceDataLink) or isinstance(data_link, DataSourceExcelSheet):
        data: pd.DataFrame = DataFileOperator(address='data_source').get(filename=alias)
    elif isinstance(data_link, DatabaseData):
        data: pd.DataFrame = DataFileOperator(address='database').get(filename=alias)
    elif isinstance(data_link, TaskResultFile):
        data: pd.DataFrame = DataFileOperator(address='application').get(filename=alias)
    else:
        data: pd.DataFrame = pd.DataFrame()
    record = data.shape[0]
    data_link.record = record
    db.session.commit()
    return record


def pd_data_overview(data: pd.DataFrame) -> list:
    overview: list = []
    dtypes: list = [(k, str(v)) for k, v in data.dtypes.to_dict().items()]
    all_count = data.shape[0]
    for column, type_ in dtypes:
        column_overview = dict(column=column, type=type_)
        data_temp: pd.DataFrame = data[[column]]
        count = data_temp.count()[column]
        column_overview['count'] = int(count)
        column_overview['na_count'] = int(all_count - count)
        if type_.startswith(('float', 'int')):
            description: pd.DataFrame = data_temp.describe()
            info = description.to_dict()[column]
            column_overview.update(info)
            column_overview['range'] = [info['min'], info['max']]
            mean_ = info['mean']
            std_ = info['std']
            try:
                column_overview['outliers_count'] = str(
                    data_temp[(data_temp[column] > mean_ + 3 * std_) | (data_temp[column] < mean_ - 3 * std_)].shape[0])
            except Exception as e:
                column_overview['outliers_count'] = str(e)
        else:
            column_overview['range'] = [str(x) for x in set(data_temp[column])]
            column_overview['outliers_count'] = '-'
        overview.append(column_overview)
    return overview


def get_data_overview(alias: str, address: str) -> list:
    # if alias.endswith('.csv'):
    #     data: pd.DataFrame = DataFileOperator(address='data_source').get(filename=alias)
    #     data_overview = pd_data_overview(data)
    #     return [data_overview]
    # file = os.path.join(DataDirectoryPath.get_data_source_path(), alias)
    # reader = pd.ExcelFile(file)
    # sheet_names: list = reader.sheet_names
    # overview = []
    # for sheet_name in sheet_names:
    #     data: pd.DataFrame = DataFileOperator(address='data_source').get(filename=alias, sheet_name=sheet_name)
    #     data_overview = pd_data_overview(data)
    #     data_overview.update(sheet_name=sheet_name)
    #     overview.append(data_overview)
    data: pd.DataFrame = DataFileOperator(address=address).get(filename=alias)
    data_overview = pd_data_overview(data)
    return data_overview


def data_overview_cale(data_link) -> list:
    if isinstance(data_link, DataSourceDataLink) or isinstance(data_link, DataSourceExcelSheet):
        address = 'data_source'
    elif isinstance(data_link, DatabaseData):
        address = 'database'
    elif isinstance(data_link, ProjectProcessData):
        address = 'project'
    else:
        return []
    alias = data_link.alias
    # data_type = data_link.data_type.data_type
    # if 'database' == data_type:
    #     return []
    # elif 'file' == data_type:
    overview = get_data_overview(alias=alias, address=address)
    alias = get_uuid_name(suffix='json')
    DataFileOperator(address='overview').put(data=overview, file_name=alias)
    data_view: DataOverview = DataOverview(alias=alias)
    db.session.add(data_view)
    db.session.commit()
    data_link.data_overview = data_view
    db.session.commit()
    return overview
