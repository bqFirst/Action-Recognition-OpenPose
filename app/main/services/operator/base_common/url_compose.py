#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/2/11 15:39
# @Author : wangweimin
# @File   : url_compose.py
# @Desc   :


from conf.data_path import ThumbnailDName, OriginalPictureDName, VideoDName, CaseDName


class PictureUrlCompose(object):

    @staticmethod
    def thumbnail(alias: str) -> str:
        return '/' + ThumbnailDName + '/' + alias

    @staticmethod
    def original(alias: str) -> str:
        return '/' + OriginalPictureDName + '/' + alias


class VideoUrlCompose(object):

    @staticmethod
    def video(alias: str) -> str:
        return '/' + VideoDName + '/' + alias


class CaseUrlCompose(object):

    @staticmethod
    def case(alias: str) -> str:
        return '/' + CaseDName + '/' + alias
