# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class GetOverdueAmt(BaseApi):
    url = '/repay/get-overdue-amt'
    data = {}
    param = data

    def set_filter(self, certNo=None, assetNo=None):
        if assetNo is not None:
            self.data["assetStatus"] = assetNo
        if certNo is not None:
            self.data["certNo"] = certNo


if __name__ == '__main__':
    t = GetOverdueAmt()
    t.set_filter(certNo="522731196408032123")
    print(t.post())
