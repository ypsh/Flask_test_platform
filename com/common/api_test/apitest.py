# -*- coding: UTF-8 -*-
"""完成对Markdown 文件接口测试用例的解析，接口请求机参数校验"""
import copy
import logging
import os

import requests
from datetime import datetime
from faker import Faker
from com.common.getPath import Path


class APITest:
    def __init__(self):
        self.path = Path().get_current_path()

    def read_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                file_lines = file.readlines()
                return file_lines
        except Exception as e:
            logging.error(repr(e))

    """删除空格、空行、换行符"""

    def pretreatment(self, file_lines: list):
        try:
            for i in range(0, len(file_lines)):
                file_lines[i] = str(file_lines[i]).replace(' ', '').replace('\n', '')
            while '' in file_lines:
                file_lines.remove('')
            return file_lines
        except Exception as e:
            logging.error(repr(e))
        finally:
            return file_lines

    """获取文件中测试用例信息"""

    def get_test_case(self, file_lines: list):
        test_case = {'api_name': '', 'request_parameters': [], 'return_parameters': [], 'normal': '',
                     'cases': []}
        try:
            i = 0
            while i < len(file_lines):
                vale = file_lines[i]
                if vale[0:5] == '##接口名':
                    test_case['api_name'] = vale[6:]
                if vale[0:5] == '-接口地址':
                    test_case['service_path'] = vale[7:]
                if vale[0:5] == '-请求方式':
                    test_case['request_type'] = vale[6:]
                if vale[0:5] == '-请求参数':
                    i = i + 3
                    while file_lines[i][0:5] != '-返回参数':
                        parameter = str(file_lines[i]).split('|')[1:6]
                        parameter[0] = str(parameter[0]).replace('-', '')
                        test_case['request_parameters'].append(parameter)
                        i += 1
                    i = i - 1
                if vale[0:5] == '-返回参数':
                    i = i + 3
                    while file_lines[i][0:5] != '-正常参数':
                        parameter = str(file_lines[i]).split('|')[1:5]
                        parameter[0] = str(parameter[0]).replace('-', '')
                        test_case['return_parameters'].append(parameter)
                        i += 1
                    i = i - 1
                if vale[0:5] == '-正常参数':
                    i = i + 2
                    parameter = ''
                    while file_lines[i][0:4] != '```':
                        parameter += file_lines[i]
                        test_case['normal'] = parameter
                        i += 1
                if vale[0:7] == '###测试用例':
                    i = i + 1
                    while i < len(file_lines):
                        case = {'name': '', 'input': [], 'expect': []}
                        if file_lines[i][0:4] == '####':
                            case['name'] = file_lines[i][4:]
                            i = i + 3
                            if file_lines[i] != '```':
                                while file_lines[i][0:4] != '```':
                                    if file_lines[i] != '```':
                                        case['input'].append(file_lines[i])
                                    i += 1
                                i = i + 3
                            else:
                                i = i + 3
                            if file_lines[i] != '```':
                                while file_lines[i][0:4] != '```' and i < len(file_lines):
                                    if file_lines[i] != '```':
                                        case['expect'].append(file_lines[i])
                                    i += 1
                        test_case['cases'].append(case)
                        i += 1
                i += 1
            return test_case
        except Exception as e:
            logging.error(repr(e))

    """获取测试文件所有信息"""

    def analysis_file(self, file_lines: list):
        test_cases = {'apis': []}
        case_index = []
        try:
            file_lines_new = self.pretreatment(file_lines)
            for i, value in enumerate(file_lines_new):
                if value[0:4] == '#模块名':
                    test_cases['model_name'] = value[5:]
                if '---' == value:
                    case_index.append(i)
            if case_index.__len__() > 1:
                for k, item in enumerate(case_index[1:]):
                    test_cases['apis'].append(self.get_test_case(file_lines[case_index[k]:item]))
                return test_cases
            else:
                return test_cases
        except Exception as e:
            logging.error(repr(e))

    """处理参数中的变量值"""

    def replace_variable(self, string):
        f = Faker('zh_cn')
        cert_no = f.ssn()
        name = f.name()
        mobile = f.phone_number()
        bank_card_no = f.credit_card_number()
        return string.replace('{{cert_no}}', cert_no).replace('{{name}}', name).replace('{{mobile}}', mobile).replace(
            '{{bank_card_no}}', bank_card_no)

    """生成常规测试用例"""

    def generat_case(self, request_parameters: list):
        cases = []
        try:
            # 空值校验
            for item in request_parameters:
                case = {'name': '', 'input': [], 'expect': []}
                if item[1] == '是':
                    case['name'] = item[0] + '为空'
                    case['input'].append(item[0] + '=空')
                    case['expect'].append(item[0])
                    cases.append(case)
            # 字段缺失校验
            for item in request_parameters:
                case = {'name': '', 'input': [], 'expect': []}
                if item[1] == '是':
                    case['name'] = item[0] + '缺失'
                    case['input'].append(item[0] + '=缺失')
                    case['expect'].append(item[0])
                    cases.append(case)
            # 字段类型校验
            for item in request_parameters:
                case = {'name': '', 'input': [], 'expect': []}
                if str(item[2]).lower() == 'string':
                    case['name'] = item[0] + '类型不匹配'
                    case['input'].append(item[0] + '=' + str(True))
                    case['expect'].append(item[0])
                    cases.append(case)
                else:
                    case['name'] = item[0] + '类型不匹配'
                    case['input'].append(item[0] + '="teststring"')
                    case['expect'].append(item[0])
                    cases.append(case)
            # 字段长度校验校验
            for item in request_parameters:
                case = {'name': '', 'input': [], 'expect': []}
                f = Faker()
                if item[4] != '':
                    rang = str(item[4]).split('-')
                    if str(item[2]).lower() == 'string' and int(rang[0]) - 1 > 0:
                        text = f.text(int(rang[0]) - 1)
                        case['name'] = item[0] + '长度过短'
                        case['input'].append(item[0] + '="' + text + '"')
                        case['expect'].append(item[0])
                        cases.append(case)
                    elif str(item[2]).lower() == 'string' and int(rang[1]) + 1 > 0:
                        text = f.text(int(rang[1]) + 1)
                        case['name'] = item[0] + '长度过长'
                        case['input'].append(item[0] + '="' + text + '"')
                        case['expect'].append(item[0])
                        cases.append(case)
                    elif str(item[2]).lower() == 'int' or str(item[2]).lower() == 'double':
                        case['name'] = item[0] + '数值小于范围'
                        case['input'].append(item[0] + '=' + str((int(rang[0]) - 1)))
                        case['expect'].append(item[0])
                        cases.append(case)

                        case = {'name': '', 'input': [], 'expect': []}
                        case['name'] = item[0] + '数值大于范围'
                        case['input'].append(item[0] + '=' + str((int(rang[1]) + 1)))
                        case['expect'].append(item[0])
                        cases.append(case)
            return cases
        except Exception as e:
            logging.error(repr(e))
            return cases

    """用例输入处理"""

    def input_handle(self, input, normal_json, parameter_type):
        try:
            if len(input) == 0:
                return normal_json
            for item in input:
                if str(item).__contains__('='):
                    temp = str(item).split('=')
                    # 自动生成的用例参数转换
                    if temp[1] == '缺失':
                        normal_json['data'].pop(temp[0])
                    elif temp[1] == '空' or temp[1] == '':
                        normal_json['data'][temp[0]] = ''
                    elif temp[1] == str(True):
                        normal_json['data'][temp[0]] = True
                    else:
                        # 测试用例文件获取到的参数按照参数类型转换（针对以下几种处理，sting,int,double,float,date,long,Boolean）
                        temp[1] = str(temp[1]).replace("'", '').replace('"', '')
                        try:
                            if str(parameter_type.get(temp[0])).lower() == 'string':
                                normal_json['data'][temp[0]] = temp[1]
                            elif str(parameter_type.get(temp[0])).lower() == 'boolean':
                                if temp[1] == 'true':
                                    normal_json['data'][temp[0]] = True
                                else:
                                    normal_json['data'][temp[0]] = False
                            elif str(parameter_type.get(temp[0])).lower() == 'int':
                                normal_json['data'][temp[0]] = int(temp[1])
                            elif str(parameter_type.get(temp[0])).lower() == 'double' or str(
                                    parameter_type.get(temp[0])).lower() == 'float':
                                normal_json['data'][temp[0]] = float(temp[1])
                            elif str(parameter_type.get(temp[0])).lower() == 'date':
                                normal_json['data'][temp[0]] = datetime.strptime(temp[1], '%Y-%m-%d')
                        except Exception as e:
                            logging.info('尝试数据格式转换报错'+repr(e))
                            normal_json['data'][temp[0]] = temp[1]
            return normal_json
        except Exception as e:
            logging.error('输入参数类型与要求参数不匹配' + repr(e))

    """返回结果校验"""

    def output_handle(self, output, response):
        try:
            try:
                if type(response)==type(str(12)):
                    response = eval(response)
            except Exception as e:
                logging.info('请求返回结果非json' + response + repr(e))
                response = {'temp': response}
            result = {'expect': [], 'actual': []}
            verification_results = []
            for item in output:
                item = str(item).replace("'", '').replace('"', '')
                if item.__contains__('=='):
                    temp = item.split('==')
                    actual_result = self.collect(response, temp[0])
                    result['expect'].append(item)
                    result['actual'].append(temp[0] + '==' + str(actual_result))
                    if str(actual_result) == temp[1]:
                        verification_results.append(True)
                    else:
                        verification_results.append(False)
                elif item.__contains__('!='):
                    temp = item.split('!=')
                    actual_result = self.collect(response, temp[0])
                    result['expect'].append(item)
                    result['actual'].append(temp[0] + '!=' + str(actual_result))
                    if str(actual_result) != temp[1]:
                        verification_results.append(True)
                    else:
                        verification_results.append(False)
                else:
                    result['expect'].append(item)
                    result['actual'].append(response)
                    if str(response).__contains__(item):
                        verification_results.append(True)
                    else:
                        verification_results.append(False)
            if False in verification_results:
                result['result'] = False
                return result
            else:
                result['result'] = True
                return result
        except Exception as e:
            logging.error('预期结果比对失败' + repr(e))

    """递归查找指定key"""

    def collect(self, dt, key):
        for k in dt:
            if k == key:
                return dt[k]
            else:
                if isinstance(dt[k], dict):
                    return self.collect(dt[k], key)

    """递归查找指定文件夹下所有测试用例"""

    def get_all_case_files(self, path):
        file_paths = []
        root_path = os.path.abspath(path)
        if os.path.isdir(path):
            files = os.listdir(path)
            for file in files:
                file_path = os.path.join(root_path, file)
                if os.path.isdir(file_path):
                    file_paths += self.get_all_case_files(file_path)
                elif file_path.endswith('.md'):
                    file_paths.append(file_path)
            return file_paths
        elif path.endswith('.md'):
            file_paths.append(path)
        return file_paths

    """执行用例"""

    def do_request(self, test_cases):
        # global normal
        report = {'apis': []}
        try:
            for item in test_cases['apis']:
                test_result = {'api_name': '', 'test_cases': []}
                # 根据模块名称获取host、ip
                base_url = 'http://172.16.0.13:8012/'
                model_name = test_cases['model_name']
                service_path = item['service_path']
                # request_type = item['request_type']
                request_parameters = item['request_parameters']
                test_result['api_name'] = item['api_name']
                # 转换服务参数列表到字典，便于后续获取参数类型
                parameters = {}
                for p in request_parameters:
                    parameters[p[0]] = p[2]
                # return_parameters = item['return_parameters']
                cases = item['cases']
                cases.extend(self.generat_case(request_parameters))
                # 考虑参数替换，返回值校验
                normal_json = self.replace_variable(item['normal'])
                url = base_url + service_path
                try:
                    normal_json = eval(normal_json)
                except Exception as e:
                    logging.error('用例json串校验不通过' + repr(e))
                    continue
                for case in cases:
                    request_json = copy.deepcopy(normal_json)
                    request_json = self.input_handle(case['input'], request_json, parameters)
                    b = datetime.now()
                    r = requests.post(url=url, json=request_json)
                    logging.info(request_json)
                    logging.info(r.json())
                    a = datetime.now()
                    use_time = (a - b).microseconds / 1000
                    logging.info('执行用例：' + item['api_name'] + '>>>>' + case['name'] + '\n')
                    print('执行用例：' + item['api_name'] + '>>>>' + case['name'])
                    verification_reqult = self.output_handle(case['expect'], r.json())
                    test_result['test_cases'].append(
                        [case['name'], url, r.status_code, request_json, r.text, verification_reqult, str(use_time),
                         r.text])
                    print(str(verification_reqult) + '\n')
                report['model_name'] = model_name
                report['apis'].append(test_result)
            return report
        except Exception as e:
            logging.info('用例执行异常' + repr(e))

    """输出测试报告到md文件"""

    def output_report(self, report):
        table_data = []
        detail_data = []
        pass_case = 0
        fail_case = 0
        use_time = report['use_time']
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report_bass_path = self.path + '/com/common/api_test/report_base.html'
        report_path = self.path + ('/static/api_report/report_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.html')
        i = 1
        for model in report['reports']:
            for api in model['apis']:
                for case in api['test_cases']:
                    table_data.append(
                        [i, i, model['model_name'], case[0], api['api_name'], case[2], str(case[5]['result']), case[6]])
                    detail_data.append(
                        [i, case[0], api['api_name'], model['model_name'], case[1], 'post', case[2], case[6],
                         str(case[5]['result']), str(case[3]), str(case[7]), case[5]['expect'], str(case[5]['actual'])])
                    if case[5]['result']:
                        pass_case += 1
                    else:
                        fail_case += 1
                    i += 1
        lines = self.read_file(report_bass_path)
        for i in range(0, len(lines)):
            lines[i] = str(lines[i]).replace('{{tabledata}}', str(table_data)).replace('{{details}}',
                                                                                       str(detail_data)).replace(
                '{{pass}}', str(pass_case)).replace('{{fail}}', str(fail_case)).replace('{{use_time}}',
                                                                                        str(use_time)).replace(
                '{{create_time}}', str(create_time))

        with open(report_path, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line)
        logging.info('测试报告生成路径：' + report_path)

    """主入口串联所有功能"""

    def run(self, path):
        reports = {'use_time': '', 'reports': []}
        files = self.get_all_case_files(path)
        b = datetime.now()
        for file in files:
            file_lines = self.read_file(file)
            testcases = self.analysis_file(file_lines)
            report = self.do_request(testcases)
            if report is not None:
                if len(report['apis']) != 0:
                    report['file_path'] = file
                    report['time'] = datetime.now().__format__('%Y-%m-%d %H:%M:%S')
                    reports['reports'].append(report)
        a = datetime.now()
        use_time = (a - b).seconds
        reports['use_time'] = str(use_time)
        self.output_report(reports)
        return True


if __name__ == '__main__':
    file_path = 'report_base.html'
    APITest().run('../..')
