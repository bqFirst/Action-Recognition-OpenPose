#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/8/7 17:53
# @Author : wangweimin
# @File   : application_operator.py
# @Desc   :

import os
import shutil

from app import db
from app.main.basic_main.custom_error import UserOperatorError, DockerContainerStartUpError, ApplicationStopError
from app.main.basic_main.error_message import ErrorMsg
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectNameRepeatedJudgement
from app.main.services.operator.base_common.docker_base_operator.docker_client import DockerClient
from app.main.services.operator.base_common.docker_base_operator.docker_actual_container_operator import \
    DockerContainerService
from app.main.services.operator.base_common.docker_base_operator.docker_actual_image_operator import DockerImageService
from app.main.services.operator.base_common.docker_base_operator.docker_actual_container_operator import \
    SklModelDataRecordService
from app.main.services.operator.database_operator.application_database_data_operator import AppDatabaseDataService
from app.main.services.operator.data_source_data_operator.application_data_source_excel_operator import \
    AppDsExcelService
from app.main.services.operator.picture_operator.application_picture_catalog_operator import AppPictureCatalogService
from app.main.services.operator.data_source_data_operator.application_data_source_csv_operator import AppDsCsvService
from app.main.services.operator.task_operator.task_operator import TaskService
from app.models import Application, ApplicationCatalog, Model, DockerImage, DockerContainer, DockerPort, \
    ModelVersion, DockerImageStatus, ApplicationStatus, Task, DockerImageFile
from app.tasks_celery.tasks_application.application_package_task import application_package
from conf.data_path import DataDirectoryPath

from .application_image_operator import ApplicationImageService


class ApplicationService(object):

    @staticmethod
    def __is_model_package_legal(models: list):
        for model in models:
            model_version: ModelVersion = model.model_version.first()
            if model_version is None:
                raise UserOperatorError(ErrorMsg.get_error_message(44))
            status_id = model_version.status_id
            if status_id in [1, 3]:
                raise UserOperatorError(ErrorMsg.get_error_message(44))

    @classmethod
    def __create_container_old(cls, user_id: int, models_id: list, appoint_port: int = None) -> DockerContainer:
        image = DockerImageService.create_plural_models(modes_id=models_id)
        docker_image: DockerImage = DockerImage(tags=image.tags[0], short_id=image.short_id, creator_id=user_id)
        db.session.add(docker_image)
        db.session.commit()
        port, container = DockerClient.run_container(image.short_id, appoint_port=appoint_port)
        if not DockerContainerService.status(short_id=container.short_id):
            DockerImageService.delete(image=docker_image)
            raise DockerContainerStartUpError(ErrorMsg.get_error_message(45))
        if not appoint_port:
            docker_port: DockerPort = DockerPort(port=port)
            db.session.add(docker_port)
            db.session.commit()
        else:
            docker_port: DockerPort = DockerPort.query.filter(DockerPort.port == appoint_port).first()
        docker_container: DockerContainer = DockerContainer(name=container.name, short_id=container.short_id,
                                                            docker_port_id=docker_port.id,
                                                            creator_id=user_id, image_id=docker_image.id)
        db.session.add(docker_container)
        db.session.commit()
        return docker_container

    @classmethod
    def __create_container(cls, user_id: int, models_id: list, appoint_port: int = None) -> DockerContainer:
        src_alias = SklModelDataRecordService.create(models_id=models_id)
        docker_file_directory = os.path.join(DataDirectoryPath.get_docker_path(), src_alias)
        image_tag: str = ObjectAcquisition.base_image(docker_image_id=1).tags  # 默认是skl环境
        image = DockerClient.get_image_by_tag(tags=image_tag)  # 实际存在的镜像，非数据库对象

        # 挂载信息创建
        mount_map = dict()
        mount_map[DataDirectoryPath.get_app_path()] = '/app/app'
        mount_map[DataDirectoryPath.get_conf_path()] = '/app/conf'
        mount_map[DataDirectoryPath.get_data_path()] = '/app/data'
        mount_map[os.path.join(DataDirectoryPath.get_docker_path(), src_alias)] = '/app/src'
        port, container = DockerClient.run_container_by_mount(image_short_id=image.short_id, mount_map=mount_map,
                                                              appoint_port=appoint_port)

        if not DockerContainerService.status(short_id=container.short_id):
            shutil.rmtree(docker_file_directory, True)
            raise DockerContainerStartUpError(ErrorMsg.get_error_message(45))
        if not appoint_port:
            docker_port: DockerPort = DockerPort(port=port)
            db.session.add(docker_port)
            db.session.commit()
        else:
            docker_port: DockerPort = DockerPort.query.filter(DockerPort.port == appoint_port).first()
        docker_container: DockerContainer = DockerContainer(alias=src_alias, short_id=container.short_id,
                                                            docker_port_id=docker_port.id,
                                                            creator_id=user_id, base_image_id=1)
        db.session.add(docker_container)
        db.session.commit()
        return docker_container

    @classmethod
    def create(cls, catalog_id: int, application_name: str, user_id: int, models_id: list):
        catalog: ApplicationCatalog = ObjectAcquisition.application_catalog_by_id(catalog_id=catalog_id)
        ObjectNameRepeatedJudgement.application_by_catalog(application_name=application_name, catalog=catalog)
        models: list = ObjectAcquisition.models_by_id(models_id=models_id)
        cls.__is_model_package_legal(models=models)

        docker_container = cls.__create_container(user_id=user_id, models_id=models_id)

        application_image: DockerImageFile = ApplicationImageService.create()
        application: Application = Application(name=application_name, creator_id=user_id, catalog_id=catalog_id,
                                               container_id=docker_container.id,
                                               application_image_id=application_image.id)
        db.session.add(application)
        db.session.commit()
        for model in models:
            application.models.append(model)
        db.session.commit()
        return application.id

    @classmethod
    def delete(cls, application_id: int):
        application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
        if 2 != application.status_id:
            raise UserOperatorError(ErrorMsg.get_error_message(33))

        # 删除任务
        task_list = application.tasks.all()
        for task in task_list:
            TaskService.delete(task_id=task.id)

        # 删除原始数据
        database_data_list = application.database_data.all()
        for database_data in database_data_list:
            AppDatabaseDataService.delete(data_link_id=database_data.id, is_forced=True)
        excel_data_list = application.excel_data.all()
        for excel_data in excel_data_list:
            AppDsExcelService.delete(data_link_id=excel_data.id, is_forced=True)
        data_source_list = application.data_links.all()
        for data_link in data_source_list:
            AppDsCsvService.delete(data_link_id=data_link.id, is_forced=True)
        picture_catalog_list = application.picture_catalogs.all()
        for picture_catalog in picture_catalog_list:
            AppPictureCatalogService.delete(catalog_id=picture_catalog.id)

        # 删除容器与镜像
        container: DockerContainer = application.container
        DockerContainerService.delete(container=container)
        ApplicationImageService.delete(application.application_image)

        # 删除应用
        db.session.delete(application)
        db.session.commit()

    @classmethod
    def get_old(cls, application_id: int) -> dict:
        application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
        application_status: ApplicationStatus = application.application_status
        container: DockerContainer = application.container

        image_status: DockerImageStatus = container.image.image_status
        return {'application_id': application_id, 'application_name': application.name,
                'creator': application.creator.name, 'create_time': application.create_time,
                'status_id': application_status.id, 'status_name': application_status.name,
                'image_status_id': image_status.id, 'image_status_name': image_status.image_status}

    @classmethod
    def get(cls, application_id: int) -> dict:
        application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
        application_status: ApplicationStatus = application.application_status
        image_status: DockerImageStatus = application.application_image.image_status

        return {'application_id': application_id, 'application_name': application.name,
                'creator': application.creator.name, 'create_time': application.create_time,
                'status_id': application_status.id, 'status_name': application_status.name,
                'image_status_id': image_status.id, 'image_status_name': image_status.image_status}

    @classmethod
    def start(cls, application_id: int):
        application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
        original_status = application.status_id
        if application.status_id == 1:
            return
        application.status_id = 3
        db.session.commit()
        container: DockerContainer = application.container
        try:
            cls.start_container(short_id=container.short_id)
            application.status_id = 1
            db.session.commit()
            return
        except Exception:
            application.status_id = original_status
            db.session.commit()
            raise

    @classmethod
    def __is_task_run(cls, application: Application):
        if application.tasks.filter(Task.status_id.in_([1, 2])).first() is not None:
            raise ApplicationStopError(ErrorMsg.get_error_message(50))

    @classmethod
    def stop(cls, application_id):
        application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
        original_status = application.status_id
        if application.status_id == 2:
            return

        # 判断是否有任务在执行
        cls.__is_task_run(application=application)

        application.status_id = 4
        db.session.commit()
        container: DockerContainer = application.container

        try:
            cls.stop_container(container.short_id)
            application.status_id = 2
            db.session.commit()
        except Exception:
            application.status_id = original_status
            db.session.commit()
            raise

    @classmethod
    def add_model(cls, application_id: int, models_id: list):
        application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
        if 2 != application.status_id:
            raise UserOperatorError(ErrorMsg.get_error_message(48))
        original_models_id: list = set([x[0] for x in application.models.with_entities(Model.id).all()])
        difference_set: set = set(models_id) - set(original_models_id)
        if not difference_set:
            return
        models: list = ObjectAcquisition.models_by_id(models_id=list(difference_set))
        cls.__is_model_package_legal(models=models)
        union_set = set.union(set(models_id), set(original_models_id))
        old_container: DockerContainer = application.container
        try:
            cls.stop_container(short_id=old_container.short_id)
            docker_container = cls.__create_container(user_id=application.creator_id, models_id=list(union_set),
                                                      appoint_port=old_container.port)
        except DockerContainerStartUpError:
            raise DockerContainerStartUpError(ErrorMsg.get_error_message(49))
        except Exception:
            raise
        application.container_id = docker_container.id
        ApplicationImageService.reset(application.application_image)

        for model in models:
            application.models.append(model)
        try:
            cls.stop_container(docker_container.short_id)
            application.status_id = 2
        except Exception:
            application.status_id = 1
            raise
        finally:
            db.session.commit()
            DockerContainerService.delete(container=old_container, keep_port=True)

    @classmethod
    def delete_model(cls, application_id: int, models_id: list):
        application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
        if 2 != application.status_id:
            raise UserOperatorError(ErrorMsg.get_error_message(51))
        original_models_id: list = set([x[0] for x in application.models.with_entities(Model.id).all()])
        intersection_set: set = set(models_id) & set(original_models_id)
        if len(intersection_set) == len(original_models_id):
            raise UserOperatorError('不支持将模型清空')
        if not intersection_set:
            return

        # 检查模型是否被使用
        error_msg_list = []
        for deleted_model in ObjectAcquisition.models_by_id(models_id=list(intersection_set)):
            run_task_name = [x[0] for x in
                             deleted_model.tasks.filter(Task.application_id == application_id).with_entities(
                                 Task.name).all()]
            if len(run_task_name) != 0:
                error_msg_list.append(
                    ErrorMsg.get_error_message(65).format(deleted_model.name, '/'.join(run_task_name)))
        if len(error_msg_list) > 0:
            raise UserOperatorError('\n'.join(error_msg_list))

        remain_set = set(original_models_id) - set(models_id)
        models: list = ObjectAcquisition.models_by_id(models_id=list(remain_set))
        cls.__is_model_package_legal(models=models)
        old_container: DockerContainer = application.container
        try:
            cls.stop_container(short_id=old_container.short_id)
            docker_container = cls.__create_container(user_id=application.creator_id, models_id=list(remain_set),
                                                      appoint_port=old_container.port)
        except DockerContainerStartUpError:
            raise DockerContainerStartUpError(ErrorMsg.get_error_message(49))
        except Exception:
            raise

        models: list = ObjectAcquisition.models_by_id(models_id=intersection_set)
        ApplicationImageService.reset(application.application_image)
        application.container_id = docker_container.id
        for model in models:
            application.models.remove(model)
        try:
            cls.stop_container(docker_container.short_id)
            application.status_id = 2
        except Exception:
            application.status_id = 1
            raise
        finally:
            db.session.commit()
            DockerContainerService.delete(container=old_container, keep_port=True)
            for model in models:
                for task in model.tasks.filter(Task.application_id == application_id).all():
                    TaskService.delete(task_id=task.id)

    @staticmethod
    def __is_package_legal_old(docker_image: DockerImage):
        if docker_image.status_id == 2:
            raise UserOperatorError(ErrorMsg.get_error_message(52))
        if docker_image.status_id == 3:
            raise UserOperatorError(ErrorMsg.get_error_message(53))

    @staticmethod
    def __is_package_legal(docker_image: DockerImageFile):
        if docker_image.status_id == 2:
            raise UserOperatorError(ErrorMsg.get_error_message(52))
        if docker_image.status_id == 3:
            raise UserOperatorError(ErrorMsg.get_error_message(53))

    @classmethod
    def package(cls, application_id: int, error=True):
        if error:
            raise UserOperatorError(ErrorMsg.get_error_message(67))
        application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
        cls.__is_package_legal(docker_image=application.application_image)
        # Todo
        # 异步任务
        # application_docker_package.delay(application_id)
        # application_docker_package(application_id)
        application_package(application_id)

    @classmethod
    def download(cls, application_id: int, error: bool = True) -> tuple:
        if error:
            raise UserOperatorError(ErrorMsg.get_error_message(67))
        application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
        docker_image: DockerImageFile = application.application_image
        if 3 != docker_image.status_id:
            raise UserOperatorError(ErrorMsg.get_error_message(54))
        alias: str = docker_image.alias

        return DataDirectoryPath.get_docker_image_path(), alias, application.name + '.zip'

    @classmethod
    def rename(cls, application_id: int, application_name: str) -> None:
        application: Application = ObjectAcquisition.application_by_id(application_id=application_id)
        if application_name == application.name:
            return
        ObjectNameRepeatedJudgement.application_by_catalog(application_name=application_name,
                                                           catalog=application.catalog)
        application.name = application_name
        db.session.commit()

    @staticmethod
    def stop_container(short_id: str):
        if not DockerContainerService.status(short_id):
            return True
        DockerContainerService.stop(short_id=short_id)
        if DockerContainerService.status(short_id):
            raise DockerContainerStartUpError(ErrorMsg.get_error_message(47))
        return True

    @staticmethod
    def start_container(short_id: str):
        if DockerContainerService.status(short_id):
            return True
        DockerContainerService.start(short_id=short_id)
        if not DockerContainerService.status(short_id):
            raise DockerContainerStartUpError(ErrorMsg.get_error_message(46))
        return True

    # @classmethod
    # def __create_container(cls, user_id: int, models_id: list, appoint_port: int = None) -> DockerContainer:
    #     print(models_id)
    #     image = DockerImageService.create_plural_models(modes_id=models_id)
    #     docker_image: DockerImage = DockerImage(tags=image.tags[0], short_id=image.short_id, creator_id=user_id)
    #     db.session.add(docker_image)
    #     db.session.commit()
    #     port, container = DockerClient.run_container(image.short_id, appoint_port=appoint_port)
    #     if not DockerContainerService.status(short_id=container.short_id):
    #         DockerImageService.delete(image=docker_image)
    #         raise DockerContainerStartUpError(ErrorMsg.get_error_message(45))
    #     if not appoint_port:
    #         docker_port: DockerPort = DockerPort(port=port)
    #         db.session.add(docker_port)
    #         db.session.commit()
    #     else:
    #         docker_port: DockerPort = DockerPort.query.filter(DockerPort.port == appoint_port).first()
    #     docker_container: DockerContainer = DockerContainer(name=container.name, short_id=container.short_id,
    #                                                         docker_port_id=docker_port.id,
    #                                                         creator_id=user_id, image_id=docker_image.id)
    #     db.session.add(docker_container)
    #     db.session.commit()
    #     return docker_container
