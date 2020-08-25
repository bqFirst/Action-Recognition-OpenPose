#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/4 14:24
# @Author : wangweimin
# @File   : task_config.py
# @Desc   :

Ip = '192.168.3.12'

Url = 'http://127.0.0.1:{}/predict?model={}'
LinuxFileCurl = 'curl -X POST "http://{}'.format(Ip) + ':{}/predict?model={}" -F "file=@local/to/data.csv"'
LinuxPictureCurl = 'curl -X POST "http://{}'.format(
    Ip) + ':{}/predict?model={}" -F "pictures=@local/to/picture1.png"  -F "pictures=@local/to/picture2.png"'
