#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/4 8:59
# @Author : wangweimin
# @File   : data_operator.py
# @Desc   :

from app.main.basic_main.custom_error import RequestValueError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.base_common.object_operator import ObjectAcquisition


class DataService(object):

    @staticmethod
    def get(data_link_id: int, data_type: str):
        """
        :return: task_type_id, data_object
        """
        if data_type in ['csv', ]:
            return 4, ObjectAcquisition.ds_data_link(data_link_id=data_link_id)
        elif 'excel' == data_type:
            return 1, ObjectAcquisition.ds_excel(data_excel_id=data_link_id)
        elif data_type in ['MySQL', ]:
            return 3, ObjectAcquisition.database_data(database_data_id=data_link_id)
        elif 'picture' == data_type:
            return 2, ObjectAcquisition.picture_catalog(catalog_id=data_link_id)
        else:
            raise RequestValueError(ErrorMsg.get_error_message(34).format(data_type))
