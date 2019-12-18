# -*- coding: UTF-8 -*-
import datetime

from com.common.jsonUtil import JsonOperate
from com.common.listUtil import ListOperate
from com.common.model import db
from com.common.model import test_case
from com.service.api_manger import ApiMangerOperate


class TestCaseOperate:
    def get_all(self, page, limit):
        return test_case.query.paginate(page, per_page=limit)

    def get_one(self, api_name):
        result = test_case.query.filter_by(api_name=api_name).first()
        if result is not None:
            return {'api_name': result.api_name, 'model': result.model, 'type': result.type,
                    'path': result.path, 'headers': result.headers, 'status': result.status, 'maker': result.mark}
        else:
            return None

    def del_case(self, case_id):
        try:
            service = test_case.query.filter_by(id=case_id).first()
            if service:
                db.session.delete(service)
                db.session.commit()
                db.session.close()
                return True
            else:
                return True
        except Exception as e:
            db.session.close()
            return True

    def get_list(self, page, limit):
        result = []
        data = self.get_all(page, limit)
        if data is not None:
            for item in data.items:
                try:
                    executeTime = item.execute_time.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    executeTime = item.execute_time
                line = {'id': item.id, 'caseName': item.case_name, 'project': item.api.model,
                        'apiName': item.api.api_name, 'requestBody': item.parameter, 'expectedResult': item.result,
                        'validationType': item.validation_type, 'remark': item.mark, 'creator': item.creater,
                        'updater': item.updater, 'executeTime': executeTime, 'executor': item.executer,
                        'result': item.last_result}

                result.append(line)
        return {'data': result, 'total': data.total}

    def get_id_by_mode(self, model):
        result = self.get_all()
        idlist = []
        if result:
            for item in result:
                if item.api.model == model:
                    idlist.append(item.id)
        return idlist

    def get_execute_list(self):
        result = []
        data = self.get_all()
        if data is not None:
            number = 1
            for item in data:
                line = [item.id, item.case_name, item.api.model, item.api.api_name, str(item.execute_time),
                        item.executer, item.last_result]
                result.append(line)
                number += 1
        return result

    def add_case(self, *args):
        global admin
        try:
            for item in args:
                if item.get('caseName') is not None:
                    api_id = ApiMangerOperate().get_id(item.get('apiName'))
                    admin = test_case(
                        case_name=item.get('caseName'),
                        parameter=JsonOperate().parameter_to_json(item.get('requestBody')),
                        result=item.get('expectedResult'),
                        validation_type=item.get('validationType'),
                        api_id=api_id,
                        creater="Admin"
                    )
                db.session.add(admin)
            db.session.commit()
            db.session.close()
            return True

        except Exception as e:
            db.session.close()
            return False

    def update_case(self, *args):
        try:
            for item in args:
                api_id = ApiMangerOperate().get_id(item.get("apiName"))
                result = test_case.query.filter_by(id=item.get("id")).first()
                if result:
                    result.case_name = item.get("caseName")
                    result.parameter = JsonOperate().parameter_to_json(item.get("requestBody"))
                    result.result = item.get("expectedResult")
                    result.validation_type = item.get("validationType")
                    result.mark = "更新"
                    result.api_id = str(api_id)
                    result.updater = "Admin"
                    result.update_time = datetime.datetime.now()
                    db.session.flush()
            db.session.commit()
            db.session.close()
            return True

        except Exception as e:
            db.session.close()
            return False

    def update_execute_result(self, *args):
        try:
            for data in args:
                for item in data:
                    result = test_case.query.filter_by(id=item['case_id']).first()
                    if result:
                        result.execute_time = item['start_time']
                        result.executer = item['creater']
                        result.last_result = item['validation_result']
                        db.session.flush()
            db.session.commit()
            db.session.close()
            return {"message": True}

        except Exception as e:
            db.session.close()
            return {"message": str(e)}

    def batch_operate(self, *args, user):
        try:
            for item in args:
                # for i in range(2,item['Sheet'])
                for n in item:
                    for i in range(2, item[n].__len__()):
                        result = test_case.query.filter_by(id=item[n][i][1]).first()
                        apis = ApiMangerOperate().get_list({"type": "id"})
                        api_id = ListOperate().get_item(apis, item[n][i][4], 0)
                        if result:
                            result.case_name = item[n][i][2]
                            result.parameter = JsonOperate().parameter_to_json(item[n][i][5])
                            result.result = item[n][i][6]
                            result.validation_type = item[n][i][7]
                            result.mark = item[n][i][8]
                            result.api_id = api_id
                            result.updater = user
                            result.update_time = datetime.datetime.now()
                            db.session.flush()
                        else:
                            db.session.add(test_case(
                                case_name=item[n][i][2],
                                parameter=JsonOperate().parameter_to_json(item[n][i][5]),
                                result=item[n][i][6],
                                validation_type=item[n][i][7],
                                mark=item[n][i][8],
                                api_id=api_id,
                                creater=user
                            ))
            db.session.commit()
            db.session.close()
            return {"message": True}

        except Exception as e:
            db.session.close()
            return {"message": str(e)}


if __name__ == '__main__':
    test_case().get_all()
