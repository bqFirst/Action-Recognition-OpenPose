#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/7/30 11:01
# @Author : wangweimin
# @File   : errors.py
# @Desc   :

from flask import render_template
from .main import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
