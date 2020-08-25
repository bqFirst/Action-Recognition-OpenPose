#! /user/bin/env python3
# coding=utf-8
# @Time   : 2019/10/24 10:44
# @Author : wangweimin
# @File   : database_operator.py
# @Desc   :

from flask_sqlalchemy import BaseQuery

from app import db
from app.main.services.core.database.databases_connect_operator import DatabasesOperator
from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectNameRepeatedJudgement
from app.models import Database, DatabaseType, Project, Application


def db_query_by_database_type_and_creator(database_type: str, creator_id: int) -> BaseQuery:
    db_type: DatabaseType = ObjectAcquisition.database_type(database_type=database_type)
    return db_type.database.filter(Database.creator_id == creator_id)


class DatabasesService(object):

    @staticmethod
    def databases_info_by_type(database_type: str, creator_id: int) -> list:
        dbs_info = []
        db_info: BaseQuery = db_query_by_database_type_and_creator(database_type=database_type, creator_id=creator_id)
        databases = db_info.all()
        for database in databases:
            db_info = dict()
            db_info['database_id'] = database.id
            db_info['name'] = database.show_name()
            dbs_info.append(db_info)
        return dbs_info


class DatabaseService(object):

    @staticmethod
    def verify(host: str, port: str, user: str, password: str, database: str, database_type: str) -> bool:
        return DatabasesOperator.verify_pool(host=host, port=port, user=user, password=password, database=database,
                                             database_type=database_type)

    @classmethod
    def create(cls, host: str, port: str, user: str, password: str, database: str, database_type: str, name: str,
               description: str, creator_id: int) -> int:
        db_type: DatabaseType = ObjectAcquisition.database_type(database_type=database_type)
        ObjectNameRepeatedJudgement.database_by_type(creator_id=creator_id, database_name=name,
                                                     database_type=db_type)
        database_: Database = Database(ip=host, port=port, user=user, password=password, database=database,
                                       db_type=db_type, name=name, description=description, creator_id=creator_id)
        db.session.add(database_)
        db.session.commit()
        return database_.id

    @classmethod
    def modify(cls, host: str, port: str, user: str, password: str, database: str, database_type: str, name: str,
               description: str, creator_id: int, database_id: int):
        db_type: DatabaseType = ObjectAcquisition.database_type(database_type=database_type)
        database_ = ObjectAcquisition.database(database_id=database_id, creator_id=creator_id,
                                               database_type=database_type)
        if database_.name != name:
            ObjectNameRepeatedJudgement.database_by_type(creator_id=creator_id, database_name=name,
                                                         database_type=db_type)
        database_.database = database
        database_.ip = host
        database_.port = port
        database_.user = user
        database_.password = password
        database_.name = name
        database_.description = description
        db.session.commit()
        DatabasesOperator.delete_pool(database=database_)

    @classmethod
    def delete(cls, database_id: int, creator_id: int) -> list:
        database = ObjectAcquisition.database(database_id=database_id, creator_id=creator_id)
        database_data_list = database.data.all()
        if database_data_list:
            result = []
            for database_data in database_data_list:
                project: Project = database_data.project
                if project is not None:
                    result.append(' / '.join(['工程', project.name, database_data.name]))
                application: Application = database_data.application
                if application is not None:
                    result.append(' / '.join(['应用', application.name, database_data.name]))
            return result
        DatabasesOperator.delete_pool(database=database)
        db.session.delete(database)
        db.session.commit()
        return []

    @classmethod
    def info(cls, database_id: int, creator_id: int) -> dict:
        database = ObjectAcquisition.database(database_id=database_id, creator_id=creator_id)
        return {'host': database.ip, 'port': database.port, 'user': database.user, 'password': database.password,
                'database': database.database, 'name': database.name, 'database_id': database.id,
                'description': database.description}

    @classmethod
    def used(cls, database_id: int, creator_id: int) -> list:
        database: Database = ObjectAcquisition.database(database_id=database_id, creator_id=creator_id)
        data_list: list = database.data.all()
        result = []
        for data in data_list:
            data_info = dict()
            # from app.models import DatabaseData
            # data: DatabaseData = None
            project: Project = data.project
            if project is not None:
                data_info['project_name'] = project.name
            application: Application = data.application
            if application is not None:
                data_info['application_name'] = application.name
            data_info['data_name'] = data.name
            result.append(data_info)
        return result
