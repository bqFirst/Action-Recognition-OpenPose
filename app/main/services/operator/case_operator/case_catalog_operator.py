#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/1/21 16:26
# @Author : wangweimin
# @File   : case_catalog_operator.py
# @Desc   :

from app import db
from app.main.basic_main.custom_error import UserOperatorError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.base_common.data_base_operator.data_transform import datetime2timestamp
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectExistJudgement, \
    ObjectNameRepeatedJudgement
from app.models import CaseCatalog, Case


class CaseCatalogService(object):

    @classmethod
    def tree(cls, catalog_id: int) -> list:
        result = []
        for case in Case.query.filter(Case.catalog_id == catalog_id).order_by(Case.name).all():
            case_msg = dict()
            case_msg['type'] = 'case'
            case_msg['name'] = case.name
            case_msg['key'] = case.key
            case_msg['case_id'] = case.id
            case_msg['create_time'] = datetime2timestamp(case.create_time)
            result.append(case_msg)
        case_catalogs: list = CaseCatalog.query.filter(CaseCatalog.pid == catalog_id).order_by(CaseCatalog.name).all()
        for case_catalog in case_catalogs:
            catalog_menu = dict()
            catalog_menu['name'] = case_catalog.name
            catalog_menu['type'] = 'catalog'
            catalog_menu['catalog_id'] = case_catalog.id
            catalog_menu['child'] = cls.tree(catalog_id=case_catalog.id)
            if '默认目录' == catalog_menu['name']:
                result.insert(0, catalog_menu)
            else:
                result.append(catalog_menu)
        return result

    @classmethod
    def create(cls, catalog_pid: int, catalog_name: str, user_id: int) -> int:
        ObjectExistJudgement.case_catalog_pid(catalog_pid=catalog_pid)
        ObjectNameRepeatedJudgement.case_catalog(catalog_name=catalog_name)
        case_catalog: CaseCatalog = CaseCatalog(name=catalog_name, pid=catalog_pid,
                                                creator_id=user_id)
        db.session.add(case_catalog)
        db.session.commit()
        return case_catalog.id

    @classmethod
    def delete(cls, catalog_id: int):
        case_catalog: CaseCatalog = ObjectAcquisition.case_catalog_by_id(catalog_id=catalog_id)

        # 判断该目录下是否有案例或目录
        if case_catalog.query.filter(
                CaseCatalog.pid == catalog_id).first() or case_catalog.cases.first() is not None:
            raise UserOperatorError(ErrorMsg.get_error_message(2))
        db.session.delete(case_catalog)
        db.session.commit()
        return

    @classmethod
    def rename(cls, catalog_id: int, catalog_name: str):
        case_catalog: CaseCatalog = ObjectAcquisition.case_catalog_by_id(catalog_id=catalog_id)
        if case_catalog.name != catalog_name:
            ObjectNameRepeatedJudgement.case_catalog(catalog_name=catalog_name)  # 不允许重名
            case_catalog.name = catalog_name
            db.session.commit()

    @classmethod
    def case_info(cls, catalog_id: int, user_id: int):
        result = []
        if 0 == catalog_id:
            cases: list = Case.query.filter(Case.creator_id == user_id).order_by(Case.name).all()
        else:
            case_catalog: CaseCatalog = ObjectAcquisition.case_catalog_by_id(catalog_id=catalog_id)
            cases = case_catalog.cases.order_by(Case.name).all()
        for case in cases:
            case_msg = dict()
            case_msg['creator'] = case.creator.name
            case_msg['case_id'] = case.id
            case_msg['create_time'] = case.create_time
            case_msg['case_name'] = case.name
            case_msg['key'] = case.key
            result.append(case_msg)
        return result
