#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/31 14:37
# @Author : wangweimin
# @File   : model_description_operator.py
# @Desc   :

from app import db
from app.main.services.operator.base_common.object_operator import ObjectAcquisition
from app.models import Model


class ModelDesService(object):

    @classmethod
    def get(cls, model_id) -> str:
        model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
        return model.description

    @classmethod
    def modify(cls, model_id: int, description: str):
        model: Model = ObjectAcquisition.model_by_id(model_id=model_id)
        model.description = description
        db.session.commit()
