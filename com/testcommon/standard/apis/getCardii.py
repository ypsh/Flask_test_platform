# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class GetCardii(BaseApi):
    url = '/cardii/get'
    data = {}
    param = data

    def set_filter(self, certNo=None):
        if certNo is not None:
            self.data["certNo"] = certNo


if __name__ == '__main__':
    t = GetCardii()
    t.set_filter(certNo="522731196408032123")
    print(t.post())
