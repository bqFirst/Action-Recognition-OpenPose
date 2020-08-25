#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/11/15 10:52
# @Author : wangweimin
# @File   : websocket_namespance.py
# @Desc   : websocket命名空间管理


Ws = '/websocket'


class WebSocketNamespace(object):

    # 工程
    ProjectModel = Ws + '/project/project/model'
    ProjectProcess = Ws + '/project/project/process'
    ProjectSource = Ws + '/project/project/source'

    # 应用
    App = Ws + '/app/app'
    Task = Ws + '/app/app/task'
    TaskLog = Ws + '/app/app/task/log'

    @classmethod
    def project_model(cls) -> str:
        return cls.ProjectModel

    @classmethod
    def project_process(cls) -> str:
        return cls.ProjectProcess

    @classmethod
    def project_source(cls) -> str:
        return cls.ProjectSource

    @classmethod
    def app_task(cls) -> str:
        return cls.Task

    @classmethod
    def task_log(cls) -> str:
        return cls.TaskLog

    @classmethod
    def app(cls) -> str:
        return cls.App
