# -*- coding: UTF-8 -*-
import configparser
import json

from flask import Blueprint, send_from_directory
from flask import render_template
from flask import request

from com.common.getPath import Path
from com.service.moker import ServiceOperate
from config.extendlink import get_titles

view = Blueprint('view', __name__)

conf = configparser.ConfigParser()
conf.read(Path().get_current_path() + '/config/config.ini', encoding='utf-8')


@view.route('/')
def start():
    return render_template('index.html')


@view.route('/dashboard')
def dashboard():
    return render_template('subtemplates/dashboard/dashboard.html')


@view.route('/extendlink')
def extendlink():
    titles = get_titles()
    return render_template('subtemplates/extendlink/extendlink.html', titles=titles)


@view.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/login.html')


@view.route('/tools/<name>', methods=['GET'])
def get_messagecode(name):
    if name == "makedata":
        return render_template('subtemplates/tools/makedata.html', name=name)
    elif name == 'aes':
        return render_template('subtemplates/tools/encryption.html', name=name)
    elif name == 'jmeter':
        return render_template('subtemplates/tools/jmeter.html', name=name)
    elif name == 'callback':
        if request.method == 'GET':
            return render_template('subtemplates/tools/callback/credit.html')
    else:
        return "building......."


@view.route('/moker', methods=['GET'])
def moker():
    return render_template('subtemplates/moker/moker.html')


@view.route('/moker/apis/<service>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def moker_service(service):
    result = ServiceOperate().get_service(service)
    if result is not None:
        if request.method == result['type'] and result['status'] != 'stop':
            return result['data']
        else:
            return json.dumps({'message': '请求方式不匹配'})


@view.route('/autotest/apimanager', methods=['GET'])
def apimanager():
    return render_template('subtemplates/autotest/apimanager.html')


@view.route('/autotest/testcase', methods=['GET'])
def testcase():
    return render_template('subtemplates/autotest/testcase.html')


@view.route('/autotest/testreport', methods=['GET'])
def testreport():
    return render_template('subtemplates/autotest/testreport.html')


@view.route('/autotest/task', methods=['GET'])
def task():
    return render_template('subtemplates/autotest/task.html')


@view.route('/datum/filesmanager', methods=['GET'])
def file_manager():
    return render_template('subtemplates/filesmanager/filesmanager.html')
