#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/3/4 10:59
# @Author : wangweimin
# @File   : ramadi_authentication.py
# @Desc   :

from flask import g, jsonify
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth, MultiAuth

from app.models import User

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='ramadi')
auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(username, password):
    g.user = None
    user: User = User.query.filter(User.name == username).first()
    if not user or not user.check_password(password):
        return False
    g.user = user
    return True


@token_auth.verify_token
def verify_token(token):
    g.user = None
    user = User.verify_auth_token(token=token)
    if user:
        g.user = user
        return True
    return False


@basic_auth.error_handler
def basic_error_handler():
    return jsonify({'code': 4011, 'msg': '用户验证失败'})


@token_auth.error_handler
def token_error_handler():
    return jsonify({'code': 4011, 'msg': '用户验证失败'})
