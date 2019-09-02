# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class GetAccountInfo(BaseApi):
    url = '/account/get-info'
    data = {}
    param = data

    def set_filter(self, certNo):
        self.data["certNo"] = certNo


if __name__ == '__main__':
    t = GetAccountInfo()
    t.set_filter("522731196408032123")
    print(t.post())
