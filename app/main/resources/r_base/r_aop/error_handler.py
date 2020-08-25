#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/22 16:43
# @Author : wangweimin
# @File   : error_handler.py
# @Desc   : 异常捕获

# import sys
import traceback

from flask import jsonify
from functools import wraps
from werkzeug.exceptions import BadRequest

from app.main.basic_main.custom_error import MyCustomError
from app.main.resources.r_base.resources_response import Response


def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # noinspection PyBroadException
        try:
            result = func(*args, **kwargs)
            return result
        except BadRequest:
            # reqparse.RequestParser()参数传递出错
            return jsonify(Response.error(message={'Error': '缺少必须参数'}))
        except MyCustomError as e:
            # if not sys.platform.startswith('linux'):
            print(traceback.format_exc())
            return jsonify(Response.error(message={'Error': str(e)}))
        except Exception:
            # if not sys.platform.startswith('linux'):
            print(traceback.format_exc())
            return jsonify(Response.error(message={'Error': '服务器繁忙，请稍后'}))
    return wrapper
