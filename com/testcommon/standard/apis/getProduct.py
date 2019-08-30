# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class GetProduct(BaseApi):
    url = '/product/get'
    data = {}
    param = data

    def set_filter(self, productNo=None):
        if productNo is not None:
            self.data["productNo"] = productNo


if __name__ == '__main__':
    t = GetProduct()
    t.set_filter(productNo="xy_1")
    print(t.post())
