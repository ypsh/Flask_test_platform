# -*- coding: UTF-8 -*-
import configparser

from com.common.getPath import Path
from com.testcommon.standard.apis.baseApi import BaseApi


class GetContract(BaseApi):

        path = Path().get_current_path()
        conf = configparser.ConfigParser()
        conf.read(path + '/config/config.ini', encoding='utf-8')
        server = conf.get('server', 'server')
        url = '/contract/get'
        data = {}
        param = data
        base_url = "http://" + server + ":8015"

        def set_filter(self, busiKey):
            self.data["busiKey"] = busiKey


if __name__ == '__main__':
    t = GetContract()
    t.set_filter("A201909021517386436827")
    print(t.post())
