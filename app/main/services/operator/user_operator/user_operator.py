#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/3/4 16:38
# @Author : wangweimin
# @File   : user_operator.py
# @Desc   :

import re

from app import db

from app.main.basic_main.custom_error import RequestValueError
from app.main.services.operator.base_common.object_operator import ObjectNameRepeatedJudgement
from app.models import User


class UserService(object):

    @classmethod
    def create(cls, username: str, password: str) -> str:
        ObjectNameRepeatedJudgement.username(username=username)
        user = User(name=username, password=password)
        db.session.add(user)
        db.session.commit()
        # Todo
        # 在该用户下创建默认目录
        return cls.get_token(user=user)

    @classmethod
    def modify(cls, username: str, telephone: str, user: User):
        if not cls.check_phone(phone=telephone):
            raise RequestValueError("手机号码错误，请重新输入")
        if user.name != username:
            ObjectNameRepeatedJudgement.username(username=username)
            user.name = username

        user.telephone = telephone
        db.session.commit()

    @staticmethod
    def get_token(user: User):
        return user.generate_auth_token().decode('ascii')

    @staticmethod
    def check_phone(phone: str) -> bool:
        if len(str(phone)) == 11:
            # 匹配手机号
            v_phone = re.match(r'^1[3-9][0-9]{9}$', phone)
            if v_phone is None:
                return False
            else:
                return True
        else:
            return False
