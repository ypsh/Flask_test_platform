# -*- coding: UTF-8 -*-
import json
import logging


# noinspection PyMethodMayBeStatic
class JsonOperate:
    def header_to_json(self, text):
        result = {}
        try:
            if text.find('{') != -1:
                return text
            for item in text.split('\n'):
                result[item.split(':')[0]] = item.split(':')[1]
            return json.dumps(result)
        except Exception as e:
            logging.error(str(e))
            return text

    def parameter_to_json(self, text):
        result = {}
        try:
            if text.find('{') != -1:
                return text
            for item in text.split('\n'):
                result[item.split(':')[0]] = item.split(':')[1]
            return json.dumps(result)
        except Exception as e:
            logging.error(str(e))
            return text
