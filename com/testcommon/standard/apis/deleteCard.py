# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class DeleteCard(BaseApi):
    url = '/card/delete'
    data = {}
    param = data

    def set_param(self, certNo, cardNo):
        self.data["certNo"] = certNo
        self.data["cardNo"] = cardNo


if __name__ == '__main__':
    t = DeleteCard()
    t.set_param(certNo="522731196408032123", cardNo="6216638241803450682")
    print(t.post())
