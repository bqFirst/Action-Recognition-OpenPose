#! /user/bin/env python3
# coding=utf-8
# @Time   : 2020/1/21 17:33
# @Author : wangweimin
# @File   : case_operator.py
# @Desc   :

from app import db

from app.main.services.operator.base_common.object_operator import ObjectAcquisition, ObjectNameRepeatedJudgement
from app.models import CaseCatalog, Case, CaseInfo, CaseDockerContainer, ParamType
from .custom_container_operator import CustomContainerService


class CaseService(object):

    @classmethod
    def create(cls, short_id: str, port: int, case_name: str, user_id: int, catalog_id: int) -> int:
        catalog: CaseCatalog = ObjectAcquisition.case_catalog_by_id(catalog_id=catalog_id)
        ObjectNameRepeatedJudgement.case_by_catalog(case_name=case_name, catalog=catalog)
        docker_container, key = CustomContainerService.create(short_id=short_id, port=port)
        case_info: CaseInfo = None
        try:
            case_info: CaseInfo = CaseInfo()
            db.session.add(case_info)
            db.session.commit()
            case: Case = Case(name=case_name, creator_id=user_id, container_id=docker_container.id, info=case_info,
                              catalog_id=catalog_id, key=key)
            db.session.add(case)
            db.session.commit()
            return case.id
        except Exception:
            if case_info is not None:
                db.session.delete(case_info)
                db.session.commit()
            CustomContainerService.delete(docker_container=docker_container)
            raise

    @classmethod
    def modify(cls, case_id: int, case_name: str, description: str, scene: str, data_trained: str, data_treatment: str,
               model_algorithm: str, model_trained: str) -> None:
        case: Case = ObjectAcquisition.case_by_id(case_id=case_id)
        if case_name != case.name:
            ObjectNameRepeatedJudgement.case_by_catalog(case_name=case_name, catalog=case.catalog)
        case.name = case_name
        case_info: CaseInfo = case.info
        case_info.description = description
        case_info.scene = scene
        case_info.data_trained = data_trained
        case_info.data_treatment = data_treatment
        case_info.model_algorithm = model_algorithm
        case_info.model_trained = model_trained
        db.session.commit()

    @classmethod
    def delete(cls, case_id: int, is_force: bool = False):
        case: Case = ObjectAcquisition.case_by_id(case_id=case_id)
        if not is_force:
            pass

        case_info: CaseInfo = case.info
        docker_container = case.container
        db.session.delete(case_info)
        db.session.delete(case)
        db.session.commit()
        CustomContainerService.delete(docker_container=docker_container)

    @classmethod
    def get(cls, case_id: int) -> dict:
        case: Case = ObjectAcquisition.case_by_id(case_id=case_id)
        case_info: CaseInfo = case.info

        docker_container: CaseDockerContainer = case.container
        param_list: list = []
        for model_mode in docker_container.model_mode.all():
            mode_dict = dict()
            mode_dict['mode_name'] = model_mode.name
            mode_dict['mode_id'] = model_mode.id
            mode_dict['input'] = []
            for input_param in model_mode.input_params.all():
                input_param_dict = dict()
                input_param_dict['param_name'] = input_param.name
                param_type: ParamType = input_param.param_type
                input_param_dict['param_type'] = param_type.name
                input_param_dict['param_type_id'] = param_type.id
                mode_dict['input'].append(input_param_dict)
            mode_dict['output'] = []
            for output_param in model_mode.output_params.all():
                output_param_dict = dict()
                output_param_dict['param_name'] = output_param.name
                param_type: ParamType = output_param.param_type
                output_param_dict['param_type'] = param_type.name
                output_param_dict['param_type_id'] = param_type.id
                mode_dict['output'].append(output_param_dict)
            param_list.append(mode_dict)
        assessment_list = []
        for model_assessment in docker_container.model_assessment:
            model_assessment_dict = dict()
            model_assessment_dict['attribute'] = model_assessment.attribute
            model_assessment_dict['value'] = model_assessment.value
            assessment_list.append(model_assessment_dict)
        return {'case_id': case_id, 'case_name': case.name, 'description': case_info.description,
                'scene': case_info.scene, 'param': param_list, 'model_assessment': assessment_list,
                'data_trained': case_info.data_trained, 'data_treatment': case_info.data_treatment,
                'model_algorithm': case_info.model_algorithm, 'model_trained': case_info.model_trained}
