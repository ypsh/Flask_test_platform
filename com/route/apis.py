# -*- coding: UTF-8 -*-
import json
import logging
import os
from concurrent.futures.thread import ThreadPoolExecutor
from urllib.parse import quote

from flask import Blueprint, request, make_response, send_from_directory
from flask_restful import Resource, Api, reqparse, fields
from werkzeug.utils import secure_filename

from com.common.aesUtil import AesUtil
from com.common.excelUtil import ExcelOperate
from com.common.getIP import SaveIP
from com.common.getPath import Path
from com.common.uploadUtil import FileUpload
from com.service.api_manger import ApiMangerOperate
from com.service.asset import Asset
from com.service.dashboard import ContCase
from com.service.executeCase import ExecuteCase
from com.service.files_manger import FilesManager
from com.service.jmeter import Jmeter
from com.service.makedata import MakdeData
from com.service.mock import ServiceOperate
from com.service.runjob import Run_job
from com.service.set_url import Set_url
from com.service.task_schedul import TaskSchedul
from com.service.test_case import TestCaseOperate
from com.service.test_report import TestReportOperate
from com.service.timeTask import TaskOperate
from com.service.user import UserOperate
from com.testcommon.api_test.apitest import APITest
from com.testcommon.standard.testcases import TestCases

executor = ThreadPoolExecutor(1)

apis = Blueprint('apis', __name__)
api = Api(apis)

resource_fields = {
    'body': fields.String,
    'result': fields.String
}

"""
系统用户处理
"""


class user(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('password', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('token', type=str, help='Rate to charge for this resource')
        self.ags = self.parser.parse_args()

    def get(self):
        result = UserOperate().get_user(self.ags['username'])
        if result is not None:
            username = AesUtil().decypt(self.ags['token']).replace(str(result['password']), '')
            if username == self.ags['username']:
                return {'status': True}
            return {'status': False}
        else:
            return {'status': False}

    def post(self):
        result = UserOperate().get_user(self.ags['username'])
        if result is not None and self.ags['password'] == str(result['password']):
            return {'login': True, 'token': AesUtil().encypt(str(result['user']) + str(result['password']))}, 200
        else:
            return {'login': False, 'token': None}, 200


"""
模拟服务，接口处理
"""


class services(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('service_name', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('service_type', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('data', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('operate', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('status', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('user', type=str, help='Rate to charge for this resource')
        self.ags = self.parser.parse_args()

    def get(self):
        data = ServiceOperate().get_mock_list()
        result = {"data": data}
        return result

    def post(self):
        result = {"message": None}
        if (self.ags['service_name'] is not None):
            if (self.ags['operate'] == 'delete'):
                result = ServiceOperate().del_item(self.ags['service_name'])
                return result
            elif (self.ags['operate'] == 'add'):
                result = ServiceOperate().add_service(
                    {'service_name': self.ags['service_name'], 'type': self.ags['service_type'],
                     'data': self.ags['data'], 'path': '/mock/apis/' + self.ags['service_name'],
                     'status': self.ags['status'], 'user': self.ags['user']})
                return result
            elif (self.ags['operate'] == 'update'):
                result = ServiceOperate().update_service(
                    {'service_name': self.ags['service_name'], 'type': self.ags['service_type'],
                     'data': self.ags['data'], 'path': '/mock/apis/' + self.ags['service_name'],
                     'status': self.ags['status'], 'user': self.ags['user']})
                return result
        return result


"""
接口管理，增删改查
"""


class api_manger(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('api_name', help='Rate to charge for this resource')
        self.parser.add_argument('model', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('type', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('path', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('headers', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('need_token', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('status', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('mark', type=str, help=' Rate to charge for this resource')
        self.parser.add_argument('user', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('operate', type=str, help='Rate to charge for this resource')
        self.ags = self.parser.parse_args()

    def get(self):
        data = ApiMangerOperate().get_list()
        result = {"data": data}
        return result

    def post(self):
        result = {"message": None}
        if (self.ags['api_name'] is not None):
            if (self.ags['operate'] == 'delete'):
                result = ApiMangerOperate().del_item(self.ags['api_name'])
                return result
            elif (self.ags['operate'] == 'add'):
                result = ApiMangerOperate().add_apis(self.ags)
                return result
            elif (self.ags['operate'] == 'update'):
                result = ApiMangerOperate().update_apis(self.ags)
                return result
        return result


"""
接口管理批量新增、更新上传处理
"""


class ApiUpload(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user', type=str, help='Rate to charge for this resource')
        self.ags = self.parser.parse_args()

    def get(self):
        return None

    def post(self):
        f = request.files['files']
        upload_path = os.path.join(Path().get_current_path(), 'static/uploads',
                                   secure_filename(f.filename))
        f.save(upload_path)
        result = ExcelOperate().get_excellist(upload_path)
        os.remove(upload_path)
        result = ApiMangerOperate().batch_operate(result, user=self.ags.user)
        return result


class test_case(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('case_name', help='Rate to charge for this resource')
        self.parser.add_argument('case_id', help='Rate to charge for this resource')
        self.parser.add_argument('servi_name', help='Rate to charge for this resource')
        self.parser.add_argument('api_id', help='Rate to charge for this resource')
        self.parser.add_argument('parameter', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('result', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('validation_type', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('mark', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('user', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('operate', type=str, help='Rate to charge for this resource')
        self.ags = self.parser.parse_args()

    def get(self):
        data = TestCaseOperate().get_list()
        result = {"data": data}
        return result

    def post(self):
        result = {"message": None}
        if (self.ags['operate'] == 'delete'):
            result = TestCaseOperate().del_case(self.ags['case_id'])
            return result
        if (self.ags['case_name'] is not None):
            if (self.ags['operate'] == 'add'):
                result = TestCaseOperate().add_case(self.ags)
                return result
            elif (self.ags['operate'] == 'update'):
                result = TestCaseOperate().update_case(self.ags)
                return result
        return result


class TestCaseUpload(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user', type=str, help='Rate to charge for this resource')
        self.ags = self.parser.parse_args()

    def get(self):
        return None

    def post(self):
        f = request.files['files']
        upload_path = os.path.join(Path().get_current_path(), 'static/uploads',
                                   secure_filename(f.filename))
        f.save(upload_path)
        result = ExcelOperate().get_excellist(upload_path)
        os.remove(upload_path)
        result = TestCaseOperate().batch_operate(result, user=self.ags.user)
        return result


"""
设置项目环境地址
"""


class set_project_url(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('project', type=str)
        self.parser.add_argument('url', type=str)
        self.ags = self.parser.parse_args()

    def get(self):
        data = Set_url().get_url(self.ags.project)
        result = {"data": data}
        return result

    def post(self):
        result = Set_url().add_url(self.ags.project, self.ags.url)
        return result


"""
执行测试用例
"""


class execute_case(Resource):
    # def __init__(self):
    #     self.parser = reqparse.RequestParser()
    #     self.parser.add_argument('data', type=str, help='Rate to charge for this resource')
    #
    #     self.ags = self.parser.parse_args()

    def get(self):
        data = TestCaseOperate().get_execute_list()
        result = {"data": data}
        return result

    def post(self):
        result = ExecuteCase().execute_cases(request.json)
        return result


"""
获取项目列表
"""


class get_modellist(Resource):
    def get(self):
        result = ApiMangerOperate().get_model_list()
        return {"data": result}


class get_reportdata(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('source', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('batchnumber', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('creater', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('executetype', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('daterange', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('type', type=str, help='Rate to charge for this resource')

        self.ags = self.parser.parse_args()

    def get(self):
        if self.ags['type'] == 'createrlist':
            result = TestReportOperate().get_createrlist()
            return {'data': result}
        else:
            result = TestReportOperate().get_report_data(self.ags)
            return result


class time_task(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('operate', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('task_id', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('task_name', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('model', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('trigger', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('start_time', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('frequency', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('until', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('user', type=str, help='Rate to charge for this resource')
        self.ags = self.parser.parse_args()

    def get(self):
        result = TaskSchedul().get_list()
        return {'message': True, 'data': result}

    def post(self):
        result = []
        if self.ags['operate'] == 'delete':
            result = TaskSchedul().del_item(self.ags['task_id'])
            return result
        elif self.ags['operate'] == 'add':
            result = TaskSchedul().add_task(self.ags)
            return result
        elif self.ags['operate'] == 'update':
            result = TaskSchedul().update_task(self.ags)
            return result


class scheduling(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('operate', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('task_id', type=str, help='Rate to charge for this resource')
        self.ags = self.parser.parse_args()

    def get(self):
        result = TaskOperate().get_jobs()
        return {'message': True, 'data': result}

    def post(self):
        if self.ags['operate'] == 'add':
            result = TaskOperate().add_jobs()
            return {'message': result, 'data': "ok"}
        if self.ags['operate'] == 'delete':
            result = TaskOperate().remove_job(self.ags['task_id'])
            return {'message': result, 'data': "ok"}


class files_manager(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('type', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('remark', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('fileid', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('filepath', type=str, help='Rate to charge for this resource')
        self.ags = self.parser.parse_args()

    def get(self):
        if self.ags['filepath'] == 'jmeter':
            path = 'jmeter/jmx'
        elif self.ags['filepath'] == 'report':
            path = 'static/report'
            result = FilesManager().get_report(path)
            if result:
                return {'message': True, 'data': result}
            else:
                return {'message': False, 'data': None}
        elif self.ags['filepath'] == 'apitest':
            path = 'com/common/api_test/testcases'
        elif self.ags['filepath'] == 'api_report':
            path = 'static/api_report'
            result = FilesManager().get_api_report(path)
            if result:
                return {'message': True, 'data': result}
            else:
                return {'message': False, 'data': None}
        elif self.ags['filepath'] == 'standard':
            path = 'static/standard'
            result = FilesManager().get_api_report(path)
            if result:
                return {'message': True, 'data': result}
            else:
                return {'message': False, 'data': None}
        else:
            path = 'static/filesmanager'
        if self.ags['type'] == 'get':
            result = FilesManager().get_list(path)
            if result:
                return {'message': True, 'data': result}
            else:
                return {'message': False, 'data': None}
        elif self.ags['type'] == 'download':
            basename = FilesManager().get_file_name(self.ags['fileid'])
            file_path = os.path.join(Path().get_current_path(), path,
                                     basename)
            dir_path = os.path.join(Path().get_current_path(), path)
            if os.path.exists(file_path):
                response = make_response(send_from_directory(dir_path, basename, as_attachment=True))
                response.headers["Content-Disposition"] = \
                    "attachment;" \
                    "filename*=UTF-8''{utf_filename}".format(
                        utf_filename=quote(basename.encode('utf-8'))
                    )
                return response
            else:
                return None

    def post(self):
        if self.ags['type'] == 'upload':
            if self.ags['filepath'] == 'jmeter':
                result = FileUpload().save_file(request.files['files'], 'jmeter/jmx')
            elif self.ags['filepath'] == 'testcase':
                result = FileUpload().save_file(request.files['files'], 'com/common/api_test/testcases')
            else:
                result = FileUpload().save_file(request.files['files'], 'static/filesmanager')
            if result:
                result['user'] = self.ags['user']
                result['remark'] = self.ags['remark']
                data = FilesManager().add_file(result)
                return {'message': data}
        elif request.json['type'] == 'delete':
            if FilesManager().del_items(json.loads(request.json['data'])):
                data = FileUpload().delete_files(json.loads(request.json['data']))
                return {'message': data}
        elif request.json['type'] == 'deletereport':
            data = FileUpload().delete_reports(json.loads(request.json['data']), path='static/report')
            return {'message': data}
        elif request.json['type'] == 'apireport':
            data = FileUpload().delete_reports(json.loads(request.json['data']), path='static/api_report')
            return {'message': data}
        elif request.json['type'] == 'smokingreport':
            data = FileUpload().delete_reports(json.loads(request.json['data']), path='static/standard')
            return {'message': data}
        elif request.json['type'] == 'remark':
            data = FilesManager().batch_update(json.loads(request.json['data']))
            return {'message': data}


class dash_board(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=str, help='Rate to charge for this resource')
        self.ags = self.parser.parse_args()

    def get(self):
        if self.ags['type'] == 'api_model_data':
            result = ContCase().get_api_model()
            if result:
                return result
            else:
                return {'message': False, 'data': None}
        elif self.ags['type'] == 'case_model_data':
            result = ContCase().get_case_model()
            if result:
                return result
        elif self.ags['type'] == 'api_case_data':
            result = ContCase().get_api_case()
            if result:
                return result
        elif self.ags['type'] == 'case_pass_data':
            result = ContCase().get_case_pass()
            if result:
                return result


"""
数据加解密
"""


class aes(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('aes', type=str, help='Rate to charge for this resource')
        self.ags = self.parser.parse_args()

    def post(self):
        result = {"message": None}
        if (self.ags['aes'] is not None):
            result = AesUtil().aes(self.ags['aes'])
        return result


"""
随机生成指定范围的个人信息
"""


class makedata(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('city', type=str)
        self.parser.add_argument('age', type=str)
        self.parser.add_argument('sex', type=str)
        self.ags = self.parser.parse_args()

    def get(self):
        data = MakdeData().get_info(self.ags)
        return {"data": data}

    def post(self):
        pass


"""
执行jmeter命令、获取执行报告
"""


class jmeter(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('jmx', type=str)
        self.ags = self.parser.parse_args()

    def get(self):
        pass

    def post(self):
        try:
            result = Jmeter().execute_jmx(json.loads(request.json['data'])[0][1])
            return result
        except:
            return {'message': False}


class apitest(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('md', type=str)
        self.parser.add_argument('path', type=str)
        self.ags = self.parser.parse_args()

    def get(self):
        pass

    def post(self):
        try:
            result = APITest().run(json.loads(request.json['data'])[0][6])
            if result:
                return {'message': True}
            else:
                return {'message': False}
        except:
            return {'message': False}


class accesslog(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.ags = self.parser.parse_args()

    def get(self):
        data = SaveIP().read_access_log()
        return {'data': data}

    def post(self):
        try:
            data = SaveIP().analysis()
            return {'message': True, 'data': data}
        except:
            return {'message': False}


class runjob(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('date', type=str)
        self.parser.add_argument('type', type=str)
        self.parser.add_argument('project_code', type=str)
        self.ags = self.parser.parse_args()

    def get(self):
        return Run_job().loadDataSet(10, self.ags.project_code)

    def post(self):
        try:
            if self.ags.type == 'getdate':
                date = Run_job().get_date(self.ags.project_code)
                return {'date': str(date)}
            else:
                result = Run_job().run(to_date=self.ags.date, project_code=self.ags.project_code)
            return result
        except:
            return {'message': False}


class run_smokingtest(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('project_code', type=str)
        self.parser.add_argument('type', type=str)
        self.ags = self.parser.parse_args()

    def get(self):
        if self.ags.type == "log":
            return TestCases().loadDataSet(20)
        return {"status": TestCases().get_status()}

    def post(self):
        try:
            result = TestCases().run_test(self.ags.project_code)
            return {"sucess": True, "message": "后台处理中，请稍后刷新查看报告"}
        except:
            return {'message': False}


class get_assets(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('project_code', type=str)
        self.parser.add_argument('type', type=str)
        self.parser.add_argument('num', type=str)
        self.parser.add_argument('asset_no', type=str)
        self.parser.add_argument('totalterm', type=str)
        self.parser.add_argument('intcaltype', type=str)
        self.ags = self.parser.parse_args()

    def get(self):
        if self.ags.type == "detail":
            return Asset().get_info(self.ags.asset_no)
        return {"data": eval(Asset().get_assets(self.ags.asset_no))}

    def post(self):
        try:
            result = Asset().incomming(self.ags.project_code, int(self.ags.num), self.ags.totalterm,
                                       self.ags.intcaltype)
            return result
        except Exception as e:
            logging.error(repr(e))
            return {'sucess': False}


api.add_resource(user, '/user')
api.add_resource(services, '/service')
api.add_resource(api_manger, '/apimanager')
api.add_resource(test_case, '/testcase')
api.add_resource(ApiUpload, '/apiupload')
api.add_resource(TestCaseUpload, '/testcaseupload')
api.add_resource(set_project_url, '/seturl')
api.add_resource(execute_case, '/executecase')
api.add_resource(get_modellist, '/modelist')
api.add_resource(get_reportdata, '/report')
api.add_resource(time_task, '/task')
api.add_resource(scheduling, '/scheduling')
api.add_resource(files_manager, '/filesmanager')
api.add_resource(dash_board, '/dashboard')
api.add_resource(aes, '/aes')
api.add_resource(makedata, '/makedata')
api.add_resource(jmeter, '/jmeter')
api.add_resource(apitest, '/apitest')
api.add_resource(accesslog, '/accesslog')
api.add_resource(runjob, '/runjob')
api.add_resource(run_smokingtest, '/runsmoking')
api.add_resource(get_assets, '/getassets')
