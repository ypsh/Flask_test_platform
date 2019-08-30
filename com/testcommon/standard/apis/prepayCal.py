# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class PrepayCal(BaseApi):
    url = '/repay/prepay-cal'
    data = {}
    param = data

    def set_filter(self, certNo=None, assetNo=None, payAmt=None):
        if certNo is not None:
            self.data["certNo"] = certNo
        if assetNo is not None:
            self.data["assetNo"] = assetNo
        if payAmt is not None:
            self.data["payAmt"] = payAmt


if __name__ == '__main__':
    t = PrepayCal()
    t.set_filter(certNo="522731196408032123", assetNo="A201908270948267944581", payAmt=12000)
    print(t.post())
