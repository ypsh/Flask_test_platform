# -*- coding: UTF-8 -*-
import datetime
import logging

from com.common.jsonUtil import JsonOperate
from com.common.model import api_manager
from com.common.model import db


# noinspection PyShadowingNames
class ApiMangerOperate:
    def get_all(self):
        return api_manager.query.all()

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
                if item.headers is not None:
                    headers = JsonOperate().header_to_json(item.headers)
                admin = api_manager(
                    api_name=item.api_name,
                    model=item.model,
                    type=item.type,
                    path=item.path,
                    status=item.status,
                    headers=str(headers).replace("'", '"'),
                    need_token=item.need_token,
                    mark=item.mark,
                    creater=item.user
                )
                db.session.add(admin)
            db.session.commit()
            db.session.close()
            return {"message": True}

        except Exception as e:
            db.session.close()
            return {"message": str(e)}

    def update_apis(self, *args):
        try:
            for item in args:
                result = api_manager.query.filter_by(
                    api_name=item['api_name']).first()
                headers = JsonOperate().header_to_json(item.headers)
                if result:
                    result.api_name = item.api_name
                    result.model = item.model
                    result.type = item.type
                    result.path = item.path
                    result.status = item.status
                    result.headers = str(headers).replace("'", '"')
                    result.need_token = item.need_token
                    result.mark = item.mark
                    result.updater = item.user
                    result.update_time = datetime.datetime.now()
                    db.session.flush()
            db.session.commit()
            db.session.close()
            return {"message": True}

        except Exception as e:
            db.session.close()
            return {"message": str(e)}

    def del_item(self, api_name):
        try:
            service = api_manager.query.filter_by(api_name=api_name).first()
            db.session.delete(service)
            db.session.commit()
            db.session.close()
            return {"message": True}
        except Exception as e:
            db.session.close()
            return {"message": str(e)}

    def get_list(self, *args):
        try:
            result = []
            data = self.get_all()
            if args.__len__():
                for item in data:
                    line = [item.id, item.api_name]
                    result.append(line)
                return result
            if data is not None:
                number = 1
                for item in data:
                    if item.cases.__len__() != 0:
                        cases = 'Yes'
                    else:
                        cases = 'No'
                    line = [number, item.api_name, item.model, item.type, item.path, item.headers, item.need_token,
                            item.status, item.mark, cases, item.updater]
                    result.append(line)
                    number += 1
            return result
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
