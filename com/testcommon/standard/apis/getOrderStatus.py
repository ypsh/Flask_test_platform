# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class GetOrderStatus(BaseApi):
    url = '/repay/get-order-status'
    data = {}
    param = data

    def set_filter(self, repayOrderNo=None):
        if repayOrderNo is not None:
            self.data["repayOrderNo"] = repayOrderNo


if __name__ == '__main__':
    t = GetOrderStatus()
    t.set_filter(repayOrderNo="120114193411291960")
    print(t.post())
