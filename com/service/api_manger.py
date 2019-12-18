# -*- coding: UTF-8 -*-
import datetime
import logging

from com.common.jsonUtil import JsonOperate
from com.common.model import api_manager
from com.common.model import db


# noinspection PyShadowingNames
class ApiMangerOperate:
    def get_all(self, page, limit):
        return api_manager.query.paginate(page, per_page=limit)

    def get_api_names(self):
        names = []
        result = api_manager.query.with_entities(api_manager.api_name).distinct().all()
        if result:
            for item in result:
                names.append(item.api_name)
        return names
    def get_api(self, api_name):
        result = api_manager.query.filter_by(api_name=api_name).first()
        if result is not None:
            return {'api_name': result.api_name, 'model': result.model, 'type': result.type,
                    'path': result.path, 'headers': result.headers, 'status': result.status, 'maker': result.mark}
        else:
            return None

    def get_id(self, api_name):
        result = api_manager.query.filter_by(api_name=api_name).first()
        if result is not None:
            return result.id
        else:
            return None

    def add_apis(self, *args):
        global headers
        try:
            for item in args:
                admin = api_manager(
                    api_name=item.get('apiName'),
                    model=item.get('project'),
                    type=item.get('requestType'),
                    path=item.get('servicePath'),
                    status=item.get('status'),
                    headers=item.get('header'),
                    need_token="No",
                    mark="",
                    creater="Admin"
                )
                db.session.add(admin)
            db.session.commit()
            db.session.close()
            return True

        except Exception as e:
            db.session.close()
            return False

    def update_apis(self, *args):
        try:
            for item in args:
                result = api_manager.query.filter_by(
                    id=item['id']).first()
                if result:
                    result.api_name = item['apiName']
                    result.model = item['project']
                    result.type = item['requestType']
                    result.path = item['servicePath']
                    result.status = item['status']
                    result.headers = item['header']
                    result.mark = '更新'
                    result.updater = 'Admin'
                    result.update_time = datetime.datetime.now()
                    db.session.flush()
            db.session.commit()
            db.session.close()
            return True

        except Exception as e:
            db.session.close()
            return False

    def del_item(self, id):
        try:
            service = api_manager.query.filter_by(id=id).first()
            db.session.delete(service)
            db.session.commit()
            db.session.close()
            return True
        except Exception as e:
            db.session.close()
            return False

    def get_list(self, page, limit):
        try:
            result = []
            data = self.get_all(page, limit)
            if data is not None:
                for item in data.items:
                    if item.cases.__len__() != 0:
                        cases = 'Yes'
                    else:
                        cases = 'No'
                    line = {'id': item.id, 'apiName': item.api_name, 'project': item.model, 'requestType': item.type,
                            'servicePath': item.path, 'header': item.headers, 'token': item.need_token,
                            'status': item.status, 'remark': item.mark, 'caseStatus': cases, 'updater': item.updater}
                    result.append(line)
            return {'data': result, 'total': data.total}
        except Exception as e:
            logging.error(str(e))
            return None

    def get_model_list(self):
        result = api_manager.query.with_entities(
            api_manager.model).distinct().all()
        models = []
        if result:
            for item in result:
                models.append(item[0])

        return models

    def batch_operate(self, *args, user):
        try:
            for item in args:
                # for i in range(2,item['Sheet'])
                for n in item:
                    for i in range(2, item[n].__len__()):
                        result = api_manager.query.filter_by(
                            api_name=item[n][i][1]).first()
                        headers = JsonOperate().header_to_json(item[n][i][5])
                        if result:
                            result.api_name = item[n][i][1]
                            result.model = item[n][i][2]
                            result.type = item[n][i][3]
                            result.path = item[n][i][4]
                            result.headers = str(headers).replace("'", '"')
                            result.need_token = item[n][i][6]
                            result.status = item[n][i][7]
                            result.mark = item[n][i][8]
                            result.updater = user
                            result.update_time = datetime.datetime.now()
                            db.session.flush()
                        else:
                            headers = JsonOperate().header_to_json(
                                item[n][i][5])
                            admin = api_manager(
                                api_name=item[n][i][1],
                                model=item[n][i][2],
                                type=item[n][i][3],
                                path=item[n][i][4],
                                headers=str(headers).replace("'", '"'),
                                need_token=item[n][i][6],
                                status=item[n][i][7],
                                mark=item[n][i][8],
                                creater=user)
                            db.session.add(admin)
            db.session.commit()
            db.session.close()
            return {"message": True}

        except Exception as e:
            db.session.close()
            return {"message": str(e)}


if __name__ == '__main__':
    api_manager().get_all()
