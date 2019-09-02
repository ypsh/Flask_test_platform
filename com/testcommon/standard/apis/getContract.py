# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class GetContract(BaseApi):
    url = '/contract/get'
    data = {}
    param = data
    base_url = "http://172.16.0.13:8015"

    def set_filter(self, busiKey):
        self.data["busiKey"] = busiKey


if __name__ == '__main__':
    t = GetContract()
    t.set_filter("A201909021517386436827")
    print(t.post())
