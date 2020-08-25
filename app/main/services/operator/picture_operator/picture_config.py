#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/12 16:54
# @Author : wangweimin
# @File   : picture_config.py
# @Desc   :

from multiprocessing import cpu_count

from app.main.services.operator.base_common.url_compose import PictureUrlCompose


# 缩略图长宽
ThumbnailHigh = 150
ThumbnailWide = 150

# 图片存储线程数
CPUCount = cpu_count()
PictureSaveThreadPoolNum = CPUCount if CPUCount > 1 else 1
