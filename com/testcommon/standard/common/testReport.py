# -*- coding: UTF-8 -*-
from com.common.redisUtil import Redis


class TestReport:
    def __init__(self):
        self.report_key = "test_result"

    def get_report_key(self):
        return self.report_key

    def set_report_key(self, key):
        self.report_key = key

    def delete_report_key(self,key):
        Redis().delete_key(key)

    def add_result(self, **kwargs):
        """
        :param kwargs: name url expect actual result param response
        :return:
        """
        result = {}
        result["name"] = kwargs.get("name")
        result["url"] = kwargs.get("url")
        result["expect"] = kwargs.get("expect")
        result["actual"] = kwargs.get("actual")
        result["result"] = kwargs.get("result")
        result["param"] = kwargs.get("param")
        result["response"] = kwargs.get("response")
        result["use_time"] = kwargs.get("use_time")
        Redis().add_list_item("test_result", result)

    def get_result(self):
        return Redis().get_list(self.report_key)
