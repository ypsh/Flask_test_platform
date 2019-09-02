# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class GetRepayPlan(BaseApi):
    url = '/repay/get-repay-plan'
    data = {}
    param = data

    def set_filter(self, assetNo=None, repayPlanStatus=None, certNo=None):
        if certNo is not None:
            self.data["certNo"] = certNo
        if assetNo is not None:
            self.data["assetNo"] = assetNo
        if repayPlanStatus is not None:
            self.data["repayPlanStatus"] = repayPlanStatus


if __name__ == '__main__':
    t = GetRepayPlan()
    t.set_filter(certNo="522731196408032123",assetNo="")
    print(t.post())
