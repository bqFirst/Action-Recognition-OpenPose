#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/9/26 15:29
# @Author : wangweimin
# @File   : main.py
# @Desc   :

from flask import Blueprint
from flask_restful import Api

main = Blueprint('main', __name__)


def add_case_demo_resource(api):
    """案例demo"""
    from app.main.resources.r_case_demo.r_camera_monitor import CameraMonitorData, CameraMonitorDistribution
    api.add_resource(CameraMonitorDistribution, '/case/demo/camera_monitor')
    api.add_resource(CameraMonitorData, '/case/demo/camera_monitor/data')

    from app.main.resources.r_case_demo.r_human_intrusion import HumanIntrusionData
    api.add_resource(HumanIntrusionData, '/case/demo/human_intrusion/data')


def init_api():
    api = Api(main)

    # 用户
    from app.main.resources.r_user.r_user import USER, USERToken
    api.add_resource(USER, '/user')
    api.add_resource(USERToken, '/user/token')

    # 数据源目录
    from app.main.resources.r_data_source.r_data_source_catalog import DSCatalog, DSCatalogOperator, DSCatalogData
    api.add_resource(DSCatalog, '/ds/catalog')
    api.add_resource(DSCatalogOperator, '/ds/catalog/<string:catalog_id>')
    api.add_resource(DSCatalogData, '/ds/catalog/<string:catalog_id>/data-link')

    # 数据源数据
    from app.main.resources.r_data_source.r_data_source_data_upload import DSDataCsv, DSDataExcel
    from app.main.resources.r_data_source.r_data_source_data import DSDataLinkOperator, DSDataLinkData, \
        DSDataLinkOverview
    api.add_resource(DSDataCsv, '/ds/data-csv')
    api.add_resource(DSDataExcel, '/ds/data-excel')
    api.add_resource(DSDataLinkOperator, '/ds/data-link/<string:data_link_id>')
    api.add_resource(DSDataLinkData, '/ds/data-link/<string:data_link_id>/data')
    api.add_resource(DSDataLinkOverview, '/ds/data-link/<string:data_link_id>/overview')

    # 数据库链接
    from app.main.resources.r_database.r_database import DATAbase, DATAbaseOperator, DATABASEUsed
    api.add_resource(DATAbase, '/db/db')
    api.add_resource(DATAbaseOperator, '/db/db/<string:database_id>')
    api.add_resource(DATABASEUsed, '/db/db/<string:database_id>/used')

    # 数据库数据
    from app.main.resources.r_database.r_database_data import DATABASEData, DatabaseDataOperator, DatabaseDataData, \
        DatabaseDataOverview
    api.add_resource(DATABASEData, '/db/data')
    api.add_resource(DatabaseDataOperator, '/db/data/<string:data_link_id>')
    api.add_resource(DatabaseDataData, '/db/data/<string:data_link_id>/data')
    api.add_resource(DatabaseDataOverview, '/db/data/<string:data_link_id>/overview')

    # 图片
    # # 图片目录
    from app.main.resources.r_picture.r_picture_catalog import PICTURECatalog, PICTURECatalogOperator, \
        PICTURECatalogLabel, PICTURECatalogPicture, PICTURECatalogPictureName
    api.add_resource(PICTURECatalog, '/pic/catalog')
    api.add_resource(PICTURECatalogOperator, '/pic/catalog/<string:catalog_id>')
    api.add_resource(PICTURECatalogLabel, '/pic/catalog/<string:catalog_id>/label')
    api.add_resource(PICTURECatalogPicture, '/pic/catalog/<string:catalog_id>/picture')
    api.add_resource(PICTURECatalogPictureName, '/pic/catalog/<string:catalog_id>/picture/name')

    # # 图片标签
    from app.main.resources.r_picture.r_picture_label import PICTURELabel, PICTURELabelOperator, PICTURELabelPicture
    api.add_resource(PICTURELabel, '/pic/label')
    api.add_resource(PICTURELabelOperator, '/pic/label/<string:label_id>')
    api.add_resource(PICTURELabelPicture, '/pic/label/<string:label_id>/picture')

    # # 图片
    # from app.main.resources.r_picture.r_picture import PICTURE
    # api.add_resource(PICTURE, '/pic/picture/<string:picture_id>/original')

    # 工程目录
    from app.main.resources.r_project.r_project_catalog import PROJECTCatalog, PROJECTCatalogOperator, \
        PROJECTCatalogProject, PROJECTCatalogModel
    api.add_resource(PROJECTCatalog, '/project/catalog')
    api.add_resource(PROJECTCatalogOperator, '/project/catalog/<string:catalog_id>')
    api.add_resource(PROJECTCatalogProject, '/project/catalog/<string:catalog_id>/project')
    api.add_resource(PROJECTCatalogModel, '/project/model')

    # 工程
    from app.main.resources.r_project.r_project import PROJECT, ProjectOperator, PROJECTEditWindow
    api.add_resource(PROJECT, '/project/project')
    api.add_resource(ProjectOperator, '/project/project/<string:project_id>')
    api.add_resource(PROJECTEditWindow, '/project/project/<string:project_id>/edit-window')

    # 工程模型
    from app.main.resources.r_project.r_project_model import ProjectModel
    api.add_resource(ProjectModel, '/project/project/<string:project_id>/model')

    # 工程原始数据
    from app.main.resources.r_project.r_project_src_data import ProjectSrcData, ProjectSrcDataOperator
    api.add_resource(ProjectSrcData, '/project/project/<string:project_id>/src-data')
    api.add_resource(ProjectSrcDataOperator, '/project/project/<string:project_id>/src-data/<string:data_link_id>')

    # 工程过程数据
    from app.main.resources.r_project.r_project_process_data import PROJECTProcessDataOperator, PROJECTProcessData, \
        PROJECTProcessDataData
    from app.main.resources.r_project.r_project_process_jupyter import ProjectDataByName, ProjectDataRoute
    api.add_resource(PROJECTProcessData, '/project/project/<string:project_id>/process-data')
    api.add_resource(PROJECTProcessDataOperator,
                     '/project/project/<string:project_id>/process-data/<string:process_data_id>')
    api.add_resource(PROJECTProcessDataData,
                     '/project/project/<string:project_id>/process-data/<string:process_data_id>/data')
    api.add_resource(ProjectDataByName, '/jupyter/project/data/file-type')
    api.add_resource(ProjectDataRoute, '/jupyter/project/data/file-type/route')

    # 建模
    from app.main.resources.r_model import MODEL, MODELOperator, MODELSrcVerify, MODELInfo, MODELDataFormat, \
        ModelDownload, MODELSrc
    # # 模型
    api.add_resource(MODEL, '/model')
    api.add_resource(MODELOperator, '/model/<string:model_id>')

    # # Github模型
    from app.main.resources.r_model_github.r_model import MODELGithub
    from app.main.resources.r_model_github.r_model import MODELOperatorGithub
    api.add_resource(MODELGithub, '/model/github')
    api.add_resource(MODELOperatorGithub, '/model/<string:model_id>')

    # # 模型源码
    api.add_resource(MODELSrc, '/model/<string:model_id>/src')
    api.add_resource(MODELSrcVerify, '/model/src-verification')
    # # 模型信息
    api.add_resource(MODELInfo, '/model/<string:model_id>/info')
    # # 模型训练数据格式
    api.add_resource(MODELDataFormat, '/model/<string:model_id>/data-format')
    # # 模型镜像操作
    api.add_resource(ModelDownload, '/model/<string:model_id>/image')

    # 应用目录
    from app.main.resources.r_application.r_application_catalog import APPLICATIONCatalog, \
        APPLICATIONCatalogApplication, APPLICATIONCatalogOperator
    api.add_resource(APPLICATIONCatalog, '/app/catalog')
    api.add_resource(APPLICATIONCatalogOperator, '/app/catalog/<string:catalog_id>')
    api.add_resource(APPLICATIONCatalogApplication, '/app/catalog/<string:catalog_id>/app')

    # 应用
    from app.main.resources.r_application.r_application import APPLICATION, ApplicationOperator, ApplicationTask, \
        ApplicationDownload, ApplicationController
    api.add_resource(APPLICATION, '/app/app')
    api.add_resource(ApplicationOperator, '/app/app/<string:application_id>')
    api.add_resource(ApplicationTask, '/app/app/<string:application_id>/task')
    api.add_resource(ApplicationDownload, '/app/app/<string:application_id>/image')
    api.add_resource(ApplicationController, '/app/app/<string:application_id>/controller')

    # 应用数据
    from app.main.resources.r_application.r_application_src_data import ApplicationSrcData, ApplicationSrcDataOperator
    api.add_resource(ApplicationSrcData, '/app/app/<string:application_id>/src-data')
    api.add_resource(ApplicationSrcDataOperator, '/app/app/<string:application_id>/src-data/<string:data_link_id>')

    # 应用模型
    from app.main.resources.r_application.r_application_model import ApplicationModel, ApplicationModelOperator
    api.add_resource(ApplicationModel, '/app/app/<string:application_id>/model')
    api.add_resource(ApplicationModelOperator, '/app/app/<string:application_id>/model')

    # 离线任务
    from app.main.resources.r_task.r_task import TASK, TaskOperator, TaskController
    api.add_resource(TASK, '/task/task')
    api.add_resource(TaskOperator, '/task/task/<string:task_id>')
    api.add_resource(TaskController, '/task/task/<string:task_id>/controller')

    # 离线任务数据
    from app.main.resources.r_task.r_task_result import TaskResultDataData, TaskResultDataOperator
    from app.main.resources.r_task.r_task_log import TaskLogOperator
    api.add_resource(TaskResultDataOperator, '/task/result-data/<string:result_data_id>')
    api.add_resource(TaskResultDataData, '/task/result-data/<string:result_data_id>/data')
    api.add_resource(TaskLogOperator, '/task/log-data/<string:task_log_id>')

    # 案例目录
    from app.main.resources.r_case.r_case_catalog import CASECatalog, CASECatalogOperator, CASECatalogCase
    api.add_resource(CASECatalog, '/case/catalog')
    api.add_resource(CASECatalogOperator, '/case/catalog/<string:catalog_id>')
    api.add_resource(CASECatalogCase, '/case/catalog/<string:catalog_id>/case')

    # 案例
    from app.main.resources.r_case.r_case import CASE, CASEOperator
    api.add_resource(CASE, '/case/case')
    api.add_resource(CASEOperator, '/case/case/<string:case_id>')

    # 案例任务
    from app.main.resources.r_case.r_case_task import CASETask
    api.add_resource(CASETask, '/case/case/<string:case_id>/task')

    # 案例demo
    add_case_demo_resource(api)

    # docker镜像
    from app.main.resources.r_docker.r_docker_image import DOCKERBaseImage, DOCKERBaseImageDownload
    api.add_resource(DOCKERBaseImage, '/docker/base-image')
    api.add_resource(DOCKERBaseImageDownload, '/docker/base-image/<string:docker_image_id>/image')

    # dask集群信息
    from app.main.resources.r_dask_cluster import DASKCluster
    api.add_resource(DASKCluster, '/message/dask/cluster')

    # socketio
    from app.main.resources.r_socketio.r_socketio_project import ProjectSocketIORefresh
    from app.main.resources.r_socketio.r_socketio_application import ApplicationSocketIORefresh
    api.add_resource(ProjectSocketIORefresh, '/socketio/project/<string:project_id>')
    api.add_resource(ApplicationSocketIORefresh, '/socketio/app/<string:application_id>')

    # 王为民测试
    # from app.main.resources.r_test_wwm.t_test_thread import TestThread
    # api.add_resource(TestThread, '/test/thread')

init_api()

# 之后注释掉views
from app.main import views
