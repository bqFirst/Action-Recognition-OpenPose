#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/9 10:05
# @Author : wangweimin
# @File   : log.py
# @Desc   :

import logging
from logging.handlers import TimedRotatingFileHandler
import os
import re

from conf.data_path import DataDirectoryPath


class Log(object):
    __logger: logging.Logger = None

    @classmethod
    def init(cls):

        dir_path: str = os.path.join(DataDirectoryPath.get_log_path(), 'flask_log')
        DataDirectoryPath.make_dirs(dir_path)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        log_file_handler = TimedRotatingFileHandler(filename=os.path.join(dir_path, 'out'), when="MIDNIGHT", interval=1)
        log_file_handler.setFormatter(formatter)
        log_file_handler.setLevel(logging.DEBUG)
        log_file_handler.suffix = "%Y-%m-%d.log"
        log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")

        log = logging.getLogger(__name__)
        # log.setLevel(logging.DEBUG)
        log.setLevel(logging.INFO)
        log.addHandler(log_file_handler)

        cls.set_logger(logger=log)

    @classmethod
    def set_logger(cls, logger: logging.Logger) -> None:
        cls.__logger = logger

    @classmethod
    def info(cls, mess: str) -> None:
        try:
            cls.__logger.info(mess)
        except AttributeError:
            cls.init()
            cls.__logger.info(mess)

    @classmethod
    def error(cls, mess: str) -> None:
        try:
            cls.__logger.error(mess)
        except AttributeError:
            cls.init()
            cls.__logger.error(mess)

    @classmethod
    def debug(cls, mess: str) -> None:
        try:
            cls.__logger.debug(mess)
        except AttributeError:
            cls.init()
            cls.__logger.debug(mess)

    @classmethod
    def warning(cls, mess: str) -> None:
        try:
            cls.__logger.warning(mess)
        except AttributeError:
            cls.init()
            cls.__logger.warning(mess)
