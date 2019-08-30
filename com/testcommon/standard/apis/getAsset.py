# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class GetAsset(BaseApi):
    url = '/asset/get'
    data = {}
    param = data

    def set_filter(self, assetStatus=None, ovdStatus=None, certNo=None,assetNo=None):
        if assetStatus is not None:
            self.data["assetStatus"] = assetStatus
        if ovdStatus is not None:
            self.data["ovdStatus"] = ovdStatus
        if certNo is not None:
            self.data["certNo"] = certNo
        if assetNo is not None:
            self.data["assetNo"] = assetNo


if __name__ == '__main__':
    t = GetAsset()
    t.set_filter(certNo="522731196408032123")
    print(t.post())
