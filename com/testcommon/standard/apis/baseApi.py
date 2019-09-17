# -*- coding: UTF-8 -*-
import configparser
import logging
import random
from datetime import datetime

import requests

from com.common.getPath import Path


class BaseApi:
    path = Path().get_current_path()
    conf = configparser.ConfigParser()
    conf.read(path + '/config/config.ini', encoding='utf-8')
    server = conf.get('server', 'server')
    param = None
    url = ""
    base_url = "http://" + server + ":8012"
    project_code = "xy"

    def set_project(self, project_code):
        self.project_code = project_code

    def set_base(self):
        self.base_param = {"system": "auto_test",
                           "projectCode": self.project_code,
                           "reqId": datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(100000, 999999)),
                           "timestamp": datetime.timestamp(datetime.now())
                           }

    def set_base_url(self, url):
        self.base_url = url

    def set_data(self):
        if self.param:
            self.base_param["data"] = self.param

    def set_url(self, url):
        self.base_url = url

    def post(self):
        try:
            self.set_base()
            self.set_data()
            b = datetime.now()
            self.r = requests.post(url=self.base_url + self.url, json=self.base_param)
            a = datetime.now()
            self.use_time = (a - b).microseconds / 1000
            logging.info("请求地址：%s\n请求参数：%s\n响应参数：%s", self.url, self.base_param, self.r.json())
            return {"param": self.base_param, "response": self.r.json(), "status": self.r.status_code,
                    "url": self.r.url, "use_time": self.use_time}
        except Exception as e:
            logging.error("请求报错：%s \n %s", repr(e), self.r.json())
            return {"param": self.base_param, "response": self.r.json(), "status": self.r.status_code,
                    "url": self.r.url, "use_time": self.use_time}
