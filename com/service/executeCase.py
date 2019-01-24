# -*- coding: UTF-8 -*-
import configparser
import datetime
import json
import logging

import requests

from com.common.compareUtil import Compare
from com.common.getPath import Path
from com.service.test_case import TestCaseOperate
from com.service.test_report import TestReportOperate

'''
接口测试用例执行、报告写入等
'''


# noinspection PyBroadException
class ExecuteCase:

    # 获取所有测试用例
    def __init__(self):
        self.cases = ''
        self.get_all_case()
        self.report = []
        self.start_time = datetime.datetime.now()
        self.end_time = datetime.datetime.now()
        self.user = 'System'
        self.executetype = 'other'
        self.env = ''
        self.globalpath = Path().get_current_path()
        self.conf = configparser.ConfigParser()
        self.conf.read(self.globalpath + '/config/config.ini')
        self.batch_number = ''
        self.fail = 0

    def get_all_case(self):
        cases = TestCaseOperate().get_all()
        if cases:
            self.cases = cases
            return cases
        return None

    def get_case_info(self, api_id):
        case_info = {}
        if self.cases is not None:
            for item in self.cases:
                if item.id == int(api_id):
                    case_info['case_id'] = api_id
                    case_info['api_id'] = item.api_id
                    case_info['case_name'] = item.case_name
                    case_info['input'] = item.parameter
                    case_info['result'] = item.result
                    case_info['validation_type'] = item.validation_type
                    case_info['api_name'] = item.api.api_name
                    case_info['headers'] = item.api.headers
                    case_info['model'] = item.api.model
                    case_info['need_token'] = item.api.need_token
                    case_info['request_type'] = item.api.type
                    case_info['request_path'] = item.api.path
                    break
        return case_info

    def do_request(self, info):
        result = None
        if self.env == '测试环境':
            url = self.conf.get('env', 'testenv')
        elif self.env == '生产环境':
            url = self.conf.get('env', 'product')
        else:
            url = self.env
        url = url + info['request_path']
        if info['input'] == '':
            info['input'] = 'None'
        if info['headers'] == '':
            info['headers'] = 'None'
        if info['need_token'] == 'Yes':
            url = url + '?access_token=' + ''
        else:
            access_token = None
        try:
            if info['request_type'].lower() == 'get':
                self.start_time = datetime.datetime.now()
                # result = requests.get(url=url, data=eval(info['input']), headers=eval(info['headers']))
                result = requests.get(url=url, headers=eval(info['headers']))
                self.end_time = datetime.datetime.now()
                return result
            elif info['request_type'].lower() == 'post':
                self.start_time = datetime.datetime.now()
                result = requests.post(url=url, headers=eval(info['headers']),
                                       json=eval(info['input']))
                self.end_time = datetime.datetime.now()

                return result
            elif info['request_type'].lower() == 'put':
                self.start_time = datetime.datetime.now()
                result = requests.put(url=url, data=eval(info['input']), headers=eval(info['headers']))
                self.end_time = datetime.datetime.now()
                return result

            elif info['request_type'].lower() == 'delete':
                self.start_time = datetime.datetime.now()
                result = requests.delete(url=url, json=eval(info['input']))
                self.end_time = datetime.datetime.now()
                return result
            else:
                return result
        except Exception as e:
            logging.error(str(e))
            return str(e)

    def execute_result(self, info, result):
        global expectresult, actualresult, actualresult, actualresult, actualresult
        if result is None:
            return False
        try:
            expectresult = json.loads(info['result'])
            actualresult = json.loads(result.text)
        except Exception as e:
            try:
                expectresult = info['result']
                actualresult = result.text
            except Exception:
                pass

        try:
            if info['validation_type'] == '相等':
                return Compare().cmp_equal(expectresult, actualresult)
            elif info['validation_type'] == '不等':
                if Compare().cmp_equal(expectresult, actualresult):
                    return False
                else:
                    return True
            elif info['validation_type'] == '包含':
                return Compare().cmp_contain(expectresult, actualresult)
            elif info['validation_type'] == '不存在':
                if Compare().cmp_contain(expectresult, actualresult):
                    return False
                else:
                    return True
            else:
                return False
        except Exception as e:
            return str(e)

    def write_report(self):
        TestReportOperate().add_report(self.report)

    def update_case(self):
        TestCaseOperate().update_execute_result(self.report)

    def execute_bycaseid(self, case_id):
        global result, report, info
        try:
            report = {}
            info = self.get_case_info(case_id)
            result = self.do_request(info)

            if result is not None:
                if self.execute_result(info, result):
                    info['validation_result'] = 'PASS'
                else:
                    info['validation_result'] = 'FAIL'
                    self.fail += 1
                report['case_id'] = info['case_id']
                report['start_time'] = self.start_time
                report['end_time'] = self.end_time
                report['input'] = info['input']
                report['expect_result'] = info['result']
                report['response_result'] = result.text
                report['response_status'] = result.status_code
                report['request_type'] = result.request.method
                report['creater'] = self.user
                report['validation_type'] = info['validation_type']
                report['validation_result'] = info['validation_result']
                report['response_path'] = result.request.url
                report['api_name'] = info['api_name']
                report['model'] = info['model']
                report['case_name'] = info['case_name']
                report['response_headers'] = str(result.headers)
                report['use_time'] = (self.end_time - self.start_time).microseconds
                report['execute_type'] = self.executetype
                report['batch_number'] = self.batch_number
            else:
                pass

            self.report.append(report)
        except Exception as e:
            info['validation_result'] = 'FAIL'
            self.fail += 1
            report['start_time'] = self.start_time
            report['end_time'] = self.end_time
            report['input'] = info['input']
            report['expect_result'] = info['result']
            report['response_result'] = result
            report['response_status'] = ''
            report['request_type'] = result.request.method
            report['creater'] = self.user
            report['validation_type'] = info['validation_type']
            report['validation_result'] = info['validation_result']
            report['response_path'] = info['request_path']
            report['api_name'] = info['api_name']
            report['model'] = info['model']
            report['case_name'] = info['case_name']
            report['response_headers'] = ''
            report['use_time'] = 0
            report['execute_type'] = self.executetype
            report['batch_number'] = self.batch_number
            self.report.append(report)

    def execute_all(self):
        try:
            for item in self.cases:
                self.execute_bycaseid(item.id)
        except Exception as e:
            logging.error(str(e)+result)

    def execute_bymodel(self, model):
        try:
            result = TestCaseOperate().get_id_by_mode(model)
            if result:
                for item in result:
                    self.execute_bycaseid(item)
        except Exception as e:
            logging.error(str(e) + result)

    def execute_cases(self, data):
        try:
            self.user = data['user']
            self.env = data['environment']
            self.executetype = data['type']
            self.batch_number = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            if data['type'].lower() == 'select':
                for item in json.loads(data['data']):
                    self.execute_bycaseid(item[0])
                self.write_report()
                self.update_case()
                # return {'message': True}
            elif data['type'].lower() == 'all':
                self.execute_all()
                self.write_report()
                self.update_case()
                # return {'message': True}
            elif data['type'].lower() == 'model':
                self.execute_bymodel(data['data'])
                self.write_report()
                self.update_case()
            return {'message': True,
                    'data': {'batch_number': self.batch_number, 'Total': self.report.__len__(),
                             'FAIL': self.fail, 'PASS': self.report.__len__() - self.fail}}
        except Exception as e:
            return {'message': False, 'error': str(e) + result,
                    'data': {'batch_number': self.batch_number, 'Total': self.report.__len__(),
                             'FAIL': self.fail, 'PASS': self.report.__len__() - self.fail}}


if __name__ == '__main__':
    ExecuteCase().get_all_case()
