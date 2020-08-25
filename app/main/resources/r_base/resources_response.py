#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/30 9:51
# @Author : wangweimin
# @File   : resources_response.py
# @Desc   :


class Response(object):

    ErrorResponse = {'code': 1}
    CorrectResponse = {'code': 0}
    ForceResponse = {'code': 2}
    NameRepeatedResponse = {'code': 3}
    DeleteRefusedResponse = {'code': 5}
    ErrorPopupResponse = {'code': 7}

    @classmethod
    def error(cls, **kwargs) -> dict:
        res = cls.ErrorResponse.copy()
        res.update(kwargs)
        return res

    @classmethod
    def correct(cls, **kwargs) -> dict:
        res = cls.CorrectResponse.copy()
        res.update(kwargs)
        return res

    @classmethod
    def force(cls) -> dict:
        return cls.ForceResponse.copy()

    @classmethod
    def name_repeated(cls) -> dict:
        return cls.NameRepeatedResponse.copy()

    @classmethod
    def delete_refused(cls, **kwargs) -> dict:
        res = cls.DeleteRefusedResponse.copy()
        res.update(kwargs)
        return res

    @classmethod
    def popup_error(cls, **kwargs) -> dict:
        res = cls.ErrorPopupResponse.copy()
        res.update(kwargs)
        return res
