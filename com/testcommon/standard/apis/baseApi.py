# -*- coding: UTF-8 -*-
import logging
import random
from datetime import datetime

import requests


class BaseApi:
    param = None
    url = ""
    base_url = "http://172.16.0.13:8012"

    def set_base(self):
        self.base_param = {"system": "auto_test",
                           "projectCode": "xy",
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
            self.r = requests.post(url=self.base_url + self.url, json=self.base_param)
            logging.info("请求参数：%s\n响应参数：%s", self.base_param, self.r.json())
            return {"param": self.base_param, "response": self.r.json(), "status": self.r.status_code,
                    "url": self.r.url}
        except Exception as e:
            logging.error("请求报错：%s \n %s", repr(e), self.r.json())
            return {"param": self.base_param, "response": self.r.json(), "status": self.r.status_code,
                    "url": self.r.url}
