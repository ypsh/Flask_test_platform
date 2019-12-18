# -*- coding: UTF-8 -*-
from sqlalchemy import func

from com.common.model import db, api_manager, test_case
# noinspection PyComparisonWithNone
from com.service.api_manger import ApiMangerOperate


class ContCase:
    def get_api_model(self):
        result = db.session.query(api_manager.model, func.count(api_manager.model)).group_by(api_manager.model).all()
        data = []
        models = []
        for item in result:
            data.append({"value": item[1], 'name': item[0]})
            models.append(item[0])
        return {'message': True, 'data': data, 'models': models}

    def get_case_model(self):
        result = db.session.query(api_manager.model, func.count(test_case.id)).filter(
            api_manager.id == test_case.api_id).group_by(api_manager.model).all()
        data = []
        models = []
        for item in result:
            data.append({"value": item[1], 'name': item[0]})
            models.append(item[0])
        return {'message': True, 'data': data, 'models': models}

    # noinspection PyPep8
    def get_api_case(self):
        data = {}
        models = ApiMangerOperate().get_model_list()
        for model in models:
            data[model] = [0, 0]
        result = ApiMangerOperate().get_list(1,100000)['data']
        for item in result:
            if item['project'] in data:
                if item['caseStatus'] == 'Yes':
                    data[item['project']][0] += 1
                elif item['caseStatus'] == 'No':
                    data[item['project']][1] += 1

        return {'message': True, 'data': data}

    def get_case_pass(self):
        data = {}
        models = ApiMangerOperate().get_model_list()
        for model in models:
            data[model] = [0, 0]
        result = db.session.query(api_manager.model, test_case.last_result, func.count(test_case.id)).filter(
            api_manager.id == test_case.api_id).group_by(test_case.api_id, test_case.last_result).all()
        for item in result:
            if item[0] in data:
                if item[1] == 'PASS':
                    data[item[0]][0] += item[2]
                elif item[1] == 'FAIL':
                    data[item[0]][1] += item[2]
        return {'message': True, 'data': data}
