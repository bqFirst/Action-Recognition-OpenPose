#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/6 16:53
# @Author : wangweimin
# @File   : setting.py
# @Desc   :


# ModelDescription % data_format
ModelDescription = "Data to predicted needed to satisfy below data format:\n%s\n\n" \
                   "Url interface is \"http://ip:port/predict\" and send data of json type as formData.\n" \
                   "The port exported in such image is 5000\n\n" \
                   "The response data is a dict of json type like \n" \
                   "{ 'data': [{ 'result': 1 }, { 'result': 2 }] } " \
                   "or {'message': 'Error: xxx' }"
