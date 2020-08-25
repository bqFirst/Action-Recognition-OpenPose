#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/20 10:35
# @Author : wangweimin
# @File   : test_task_temp.py
# @Desc   : 每次集成异步任务需在app/tasks_celery/__init__.py中导入

import requests

from app.celery_app import celery, db, socketio
from app.models import DataSourceCatalog
from conf.system_config import ServerAddress


class Test(object):

    @celery.task
    def a(self):
        return '12'  # 必须为可json化数据


@celery.task
def test_task(catalog_name, pid, user_id):  # 必须为可json化数据

    ds = DataSourceCatalog.query.get(1)
    print(ds)
    # catalog: DataSourceCatalog = DataSourceCatalog(name=catalog_name, pid=pid, creator_id=user_id)
    # error
    # db.session.add(catalog)
    # db.session.commit()
    TestQuanju.append()
    requests.put('http://{}/socketio/project/1'.format(ServerAddress.get_address()), data={'address': 'aaa'})


class TestQuanju(object):
    t = []

    @classmethod
    def append(cls):
        cls.t.append('a')
        print(cls.t)
