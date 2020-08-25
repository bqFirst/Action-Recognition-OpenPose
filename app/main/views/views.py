#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/7/30 11:01
# @Author : wangweimin
# @File   : views.py
# @Desc   :

from flask import render_template

from app.main.main import main


@main.route('/')
@main.route('/index')
def index():
    return render_template('application.html')


@main.route('/user/<username>')
def hello(username):
    return render_template('hello.html', name=username)
