# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class CalculateRepayPlan(BaseApi):
    url = '/core/get-core-sys-date'
    data = {}
    param = data

    def set_param(self, applyAmt, productNo, totalTerm, yearRate, startDate=None, intCalcType="eq_prin_int"):
        if startDate is not None:
            self.data["startDate"] = startDate
        self.data["applyAmt"] = applyAmt
        self.data["productNo"] = productNo
        self.data["totalTerm"] = totalTerm
        self.data["yearRate"] = yearRate


if __name__ == '__main__':
    t = CalculateRepayPlan()
    t.set_param(applyAmt=1000, productNo="xy_1", totalTerm=3, yearRate=0.18)
    print(t.post())
