# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class GetContract(BaseApi):
    url = '/contract/get'
    data = {}
    param = data
    def new_url(self):
        self.set_base_url("http://172.16.0.13:8015")
    def set_param(self, busiKey):
        self.new_url()
        self.data["busiKey"] = busiKey

if __name__ == '__main__':
    t = GetContract()
    t.set_param( "A201908270948267650381")
    print(t.post())
