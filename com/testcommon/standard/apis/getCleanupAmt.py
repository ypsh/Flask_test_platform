# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class GetCleanupAmt(BaseApi):
    url = '/repay/get-cleanup-amt'
    data = {}
    param = data

    def set_filter(self, certNo=None, assetNo=None):
        if assetNo is not None:
            self.data["assetStatus"] = assetNo
        if certNo is not None:
            self.data["certNo"] = certNo


if __name__ == '__main__':
    t = GetCleanupAmt()
    t.set_filter(certNo="522731196408032123")
    print(t.post())
