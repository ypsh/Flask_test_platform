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


@view.route('/mock/apis/<path:service>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mock_service(service):
    result = ServiceOperate().get_service(service)
    if result is not None:
        if request.method == result['type'] and result['status'] != 'stop':
            return result['data']
        else:
            return json.dumps({'message': '请求方式不匹配'})

