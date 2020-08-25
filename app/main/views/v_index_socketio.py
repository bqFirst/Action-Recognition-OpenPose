#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/14 16:00
# @Author : wangweimin
# @File   : v_index_socketio.py
# @Desc   :

import time

from app.main.main import main
from flask import render_template, jsonify
from app import socketio
from flask_socketio import emit  # 新加入的代码
from threading import Lock
import random

# 新加入的代码-开始
thread = None
thread_lock = Lock()


def background_thread(user_to_json):
    """Example of how to send server generated events to clients."""
    while True:
        users_to_json = [{'name': '王腾' + str(random.randint(1, 100))}]
        socketio.sleep(0.5)  # 每五秒发送一次
        socketio.emit('user_response', {'data': users_to_json}, namespace='/websocket/user_refresh')


# @socketio.on('connect', namespace='/websocket/user_refresh')
# def connect():
#     """ 服务端自动发送通信请求 """
#     global thread
#     user_to_json = ''
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(background_thread, (user_to_json,))
#     emit('server_response', {'data': '试图连接客户端！'})
#
#
@socketio.on('connect_event', namespace='/websocket/user_refresh')
def refresh_message(message):
    """ 服务端接受客户端发送的通信请求 """
    print('server_response')
    emit('server_response', {'data': message['data']})


# 新加入的代码-结束

@main.route('/socketio', methods=['GET'])
def index2():
    return render_template('index_socketio.html')


@main.route('/socketio/start', methods=['GET'])
def socket_start():
    socketio.start_background_task(background_thread, ('',))
    sleep = random.randint(10, 16)
    time1 = time.time()
    time.sleep(sleep)
    print(time.time() - time1)
    return jsonify({'code': sleep})
