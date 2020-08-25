#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/6 16:00
# @Author : wangweimin
# @File   : data_overview_operator.py
# @Desc   :

from app import db
from app.main.services.core.data.data_file.data_file_operator import DataFileOperator
from app.main.services.operator.base_common.data_base_operator.data_cale import data_overview_cale
from app.models import DataOverview


class DataOverviewService(object):

    @classmethod
    def get(cls, data_link) -> list:
        data_overview: DataOverview = data_link.data_overview
        if data_overview is not None:
            data_overview_alias: str = data_overview.alias
            data = DataFileOperator(address='overview').get(filename=data_overview_alias)
        else:
            data = data_overview_cale(data_link=data_link)
        return data

    @classmethod
    def delete(cls, data_link):
        data_overview: DataOverview = data_link.data_overview
        if data_overview is not None:
            DataFileOperator(address='overview').delete(file_name=data_overview.alias)
            db.session.delete(data_overview)
            db.session.commit()
