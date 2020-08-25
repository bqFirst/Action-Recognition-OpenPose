#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/31 9:54
# @Author : wangweimin
# @File   : object_acquisition.py
# @Desc   :

from sqlalchemy import and_

from app.main.basic_main.custom_error import RequestIdError, RequestValueError, DockerContainerCheckError
from app.models import *


class ObjectAcquisition(object):

    @staticmethod
    def project_catalog_by_id(catalog_id: int) -> ProjectCatalog:
        project_catalog: ProjectCatalog = ProjectCatalog.query.get(catalog_id)
        if project_catalog is None:
            raise RequestIdError('Error catalog id')
        return project_catalog

    @staticmethod
    def model_by_id(model_id: int) -> Model:
        model: Model = Model.query.get(model_id)
        if not model:
            raise RequestIdError('Invalid model id')
        return model

    @staticmethod
    def project_by_id(project_id: int) -> Project:
        project = Project.query.get(project_id)
        if project is None:
            raise RequestIdError('Error project id')
        return project

    @staticmethod
    def data_type_by_name(data_type: str) -> DataType:
        data_type: DataType = DataType.query.filter(DataType.data_type == data_type).first()
        if data_type is None:
            raise RequestValueError('Error data type')
        return data_type

    @staticmethod
    def database(database_id: int, creator_id: int, database_type: str = None) -> Database:
        database: Database = Database.query.get(database_id)
        if database is None or database.creator_id != creator_id:
            raise RequestIdError('Error database id or permission denied!')
        if database_type is not None and database.db_type.db_type != database_type:
            raise RequestValueError('Error database type {}'.format(database_type))
        return database

    @staticmethod
    def database_type(database_type: str) -> DatabaseType:
        db_type: DatabaseType = DatabaseType.query.filter(DatabaseType.db_type == database_type).first()
        if db_type is None:
            raise RequestValueError('Error database type')
        return db_type

    @staticmethod
    def ds_data_link(data_link_id: int, ascription='every') -> DataSourceDataLink:
        data_link: DataSourceDataLink = DataSourceDataLink.query.get(data_link_id)
        if not data_link or not check_data_ascription(data_link, ascription=ascription):
            raise RequestIdError('Error data link id')

        return data_link

    @classmethod
    def ds_data_link_by_type(cls, data_link_id: int, data_type: str) -> DataSourceDataLink:
        data_type: DataType = cls.data_type_by_name(data_type=data_type)
        data_link: DataSourceDataLink = DataSourceDataLink.query.filter(
            and_(DataSourceDataLink.id == data_link_id, DataSourceDataLink.data_type_id == data_type.id)).first()
        if data_link is None:
            raise RequestIdError('Error data link id')
        return data_link

    @staticmethod
    def ds_excel(data_excel_id: int, ascription='every') -> DataSourceExcelSheet:
        data_excel: DataSourceExcelSheet = DataSourceExcelSheet.query.get(data_excel_id)
        if not data_excel or not check_data_ascription(data_excel, ascription=ascription):
            raise RequestIdError('Error data link id')
        return data_excel

    @staticmethod
    def database_data(database_data_id: int, ascription='every') -> DatabaseData:
        database_data: DatabaseData = DatabaseData.query.get(database_data_id)
        if database_data is None or not check_data_ascription(database_data, ascription=ascription):
            raise RequestIdError('Error data link id')
        return database_data

    @classmethod
    def picture_catalog(cls, catalog_id, ascription='every') -> PictureCatalog:
        picture_catalog: PictureCatalog = PictureCatalog.query.get(catalog_id)
        if picture_catalog is None or not check_data_ascription(picture_catalog, ascription=ascription):
            raise RequestIdError('Error catalog id')
        return picture_catalog

    @classmethod
    def picture_label(cls, catalog_id: int, label_id: int) -> PictureLabel:
        label: PictureLabel = PictureLabel.query.filter(
            and_(PictureLabel.picture_catalog_id == catalog_id, PictureLabel.id == label_id)).first()
        if label is None:
            raise RequestIdError('Error catalog id')
        return label

    @classmethod
    def picture_by_id(cls, picture_id: int, catalog_id: int = None) -> Picture:
        picture: Picture = Picture.query.get(picture_id)
        if picture is None:
            raise RequestIdError('Error picture id')
        if catalog_id is not None and picture.picture_catalog_id != catalog_id:
            raise RequestIdError('Error catalog id')
        return picture

    @classmethod
    def project_process_data(cls, project_id: int, process_data_id: int) -> ProjectProcessData:
        process_data: ProjectProcessData = ProjectProcessData.query.get(process_data_id)
        if process_data is None or process_data.project_id != project_id:
            raise RequestIdError('Error project id or process data id')
        return process_data

    @staticmethod
    def application_by_id(application_id: int) -> Application:
        application = Application.query.get(application_id)
        if application is None:
            raise RequestIdError('Error application id')
        return application

    @staticmethod
    def application_catalog_by_id(catalog_id) -> ApplicationCatalog:
        application_catalog: ApplicationCatalog = ApplicationCatalog.query.get(catalog_id)
        if application_catalog is None:
            raise RequestIdError('Error catalog id')
        return application_catalog

    @staticmethod
    def models_by_id(models_id) -> list:
        models: list = Model.query.filter(Model.id.in_(models_id)).all()
        if len(models_id) != len(models):
            raise RequestIdError('Error model id')
        return models

    @staticmethod
    def task_by_id(task_id) -> Task:
        task: Task = Task.query.get(task_id)
        if task is None:
            raise RequestIdError('Error task id')
        return task

    @staticmethod
    def task_result_file_by_id(task_result_file_id) -> TaskResultFile:
        task_result_data: TaskResultFile = TaskResultFile.query.get(task_result_file_id)
        if task_result_data is None:
            raise RequestIdError('Error task result file id')
        return task_result_data

    @classmethod
    def task_log_by_id(cls, task_log_id) -> TaskLogFile:
        task_log: TaskLogFile = TaskLogFile.query.get(task_log_id)
        if task_log is None:
            raise RequestIdError('Error task log id')
        return task_log

    @staticmethod
    def model_by_application(model_id: int, application: Application) -> Model:
        model: Model = application.models.filter(Model.id == model_id).first()
        if model is None:
            raise RequestIdError('Error model id')
        return model

    @staticmethod
    def base_image(docker_image_id) -> BaseDockerImage:
        base_image: BaseDockerImage = BaseDockerImage.query.get(docker_image_id)
        if base_image is None:
            raise RequestIdError('Error docker base image id')
        return base_image

    @staticmethod
    def case_catalog_by_id(catalog_id):
        case_catalog: CaseCatalog = CaseCatalog.query.get(catalog_id)
        if case_catalog is None:
            raise RequestIdError('Error catalog id')
        return case_catalog

    @classmethod
    def param_type(cls, param_type: str) -> ParamType:
        param_type_ = ParamType.query.filter(ParamType.name == param_type).first()
        if param_type_ is None:
            raise DockerContainerCheckError('Error param type')
        return param_type_

    @classmethod
    def case_by_id(cls, case_id) -> Case:
        case: Case = Case.query.get(case_id)
        if case is None:
            raise RequestIdError('Error case id')
        return case

    @classmethod
    def mode_by_container(cls, mode_id: int, docker_container: DockerContainer) -> DockerModelMode:
        model_mode: DockerModelMode = docker_container.model_mode.filter(DockerModelMode.id == mode_id).first()
        if model_mode is None:
            raise RequestValueError('Error mode id')
        return model_mode


def check_data_ascription(data_link, ascription: str) -> bool:
    if 'project' == ascription:
        if data_link.projects.first() is None:
            return False
    elif 'application' == ascription:
        if data_link.applications.first() is None:
            return False
    elif 'every' == ascription:
        return True
    else:
        return False
    return True
