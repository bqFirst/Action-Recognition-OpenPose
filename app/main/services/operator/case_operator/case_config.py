#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/1/22 15:59
# @Author : wangweimin
# @File   : case_config.py
# @Desc   :

from conf.system_config import Settings

Url = 'http://{}'.format(Settings['docker.ip']) + ':{}'
InitUrl = Url + '/init_status'
PredictUrl = Url + '/predict'
ParamUrl = Url + '/param'
