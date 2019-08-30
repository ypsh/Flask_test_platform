# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class UpdateCard(BaseApi):
    url = '/card/update-binding'
    data = {}
    param = data

    def set_param(self, **kwargs):
        self.data["certNo"] = kwargs.get("certNo")
        self.data["cardNo"] = kwargs.get("cardNo")
        self.data["oldCardNo"] = kwargs.get("oldCardNo")
        self.data["name"] = kwargs.get("name")
        self.data["mobile"] = kwargs.get("mobile")
        self.data["bankName"] = kwargs.get("bankName")
        self.data["bankCode"] = kwargs.get("bankCode")
        self.data["type"] = kwargs.get("type")
        if kwargs.get("unionMark") is not None:
            self.data["unionMark"] = kwargs.get("unionMark")


if __name__ == '__main__':
    t = UpdateCard()
    t.set_param(certNo="522731196408032123",
                oldCardNo="620622193010055460",
                cardNo="6216638241803450699",
                name="黄梅",
                mobile="123146546",
                bankName="广大音乐",
                bankCode="6213",
                unionMark="0",
                type="debit"
                )
    print(t.post())
