# -*- coding: UTF-8 -*-
import configparser
import json
import os

from flask import Blueprint
from flask import render_template
from flask import request

from com.common.getIP import SaveIP
from com.common.getPath import Path
from com.service.mock import ServiceOperate
from config.extendlink import get_titles

view = Blueprint('view', __name__)

conf = configparser.ConfigParser()
conf.read(Path().get_current_path() + '/config/config.ini', encoding='utf-8')
globalspath = Path().get_current_path()


@view.route('/')
def start():
    SaveIP().save(request.headers, page='home')
    return render_template('index.html')


@view.route('/dashboard')
def dashboard():
    SaveIP().save(request.headers, page='dashboard')
    return render_template('subtemplates/dashboard/dashboard.html')


@view.route('/extendlink')
def extendlink():
    SaveIP().save(request.headers, page='extendlink')
    titles = get_titles()
    return render_template('subtemplates/extendlink/extendlink.html', titles=titles)


@view.route('/login', methods=['GET', 'POST'])
def login():
    SaveIP().save(request.headers, page='login')
    if request.method == 'GET':
        return render_template('/login.html')


@view.route('/tools/<name>', methods=['GET'])
def tools(name):
    SaveIP().save(request.headers, page='tool')
    if name == "makedata":
        return render_template('subtemplates/tools/makedata.html', name=name)
    elif name == 'aes':
        return render_template('subtemplates/tools/encryption.html', name=name)
    elif name == 'jmeter':
        return render_template('subtemplates/tools/jmeter.html', name=name)
    elif name == 'apitest':
        return render_template('subtemplates/tools/apitest.html', name=name)
    elif name == 'bankcode':
        return render_template('subtemplates/tools/bankcode.html', name=name)
    elif name == 'accesslog':
        return render_template('subtemplates/tools/accesslog.html', name=name)
    elif name == 'smokingtest':
        return render_template('subtemplates/tools/smokingtest.html', name=name)
    elif name == 'runjob':
        return render_template('subtemplates/tools/runjob.html', name=name)
    elif name == 'callback':
        if request.method == 'GET':
            return render_template('subtemplates/tools/callback/credit.html')
    else:
        return "building......."


@view.route('/mock', methods=['GET'])
def mock():
    SaveIP().save(request.headers, page='mock')
    return render_template('subtemplates/mock/mock.html')


@view.route('/mock/apis/<path:service>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mock_service(service):
    result = ServiceOperate().get_service(service)
    if result is not None:
        if request.method == result['type'] and result['status'] != 'stop':
            return result['data']
        else:
            return json.dumps({'message': '请求方式不匹配'})


@view.route('/autotest/apimanager', methods=['GET'])
def apimanager():
    SaveIP().save(request.headers, page='apimanager')
    return render_template('subtemplates/autotest/apimanager.html')


@view.route('/autotest/testcase', methods=['GET'])
def testcase():
    SaveIP().save(request.headers, page='testcase')
    return render_template('subtemplates/autotest/testcase.html')


@view.route('/autotest/testreport', methods=['GET'])
def testreport():
    SaveIP().save(request.headers, page='testreport')
    return render_template('subtemplates/autotest/testreport.html')


@view.route('/autotest/task', methods=['GET'])
def task():
    SaveIP().save(request.headers, page='task')
    return render_template('subtemplates/autotest/task.html')


@view.route('/datum/filesmanager', methods=['GET'])
def file_manager():
    SaveIP().save(request.headers, page='filesmanager')
    return render_template('subtemplates/filesmanager/filesmanager.html')


@view.route('/log/<string:log_name>')
def log(log_name):
    body = []
    log_file = os.path.join(globalspath, 'myapp.log')
    if os.path.exists(log_file):
        body = open(log_file, 'r').readlines()
    else:
        pass
    html_body = '\n'.join('<p>%s</p>' % line for line in body)
    return render_template('subtemplates/tools/logs.html', body=html_body, job_id=log_name)
