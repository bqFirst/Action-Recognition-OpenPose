#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/12/20 10:35
# @Author : wangweimin
# @File   : __init__.py.py
# @Desc   :

from app.tasks_celery.test_task_temp import *
from app.tasks_celery.tasks_model.model_train_task import *
from app.tasks_celery.tasks_model.model_package_task import *
from app.tasks_celery.docker_package_task import *
