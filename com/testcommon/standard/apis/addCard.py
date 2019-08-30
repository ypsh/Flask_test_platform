# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class AddCard(BaseApi):
    url = '/card/add'
    data = {}
    param = data

    def set_param(self, args):
        self.data["certNo"] = args.get("certNo")
        self.data["cardNo"] = args.get("cardNo")
        self.data["name"] = args.get("name")
        self.data["mobile"] = args.get("mobile")
        self.data["bankName"] = args.get("bankName")
        self.data["bankCode"] = args.get("bankCode")
        self.data["type"] = args.get("type")
        if args.get("unionMark") is not None:
            self.data["unionMark"] = args.get("unionMark")


if __name__ == '__main__':
    t = AddCard()
    t.set_param({"certNo": "522731196408032123",
                 "cardNo": "6216638241803450699",
                 "name": "黄梅",
                 "mobile": "123146546",
                 "bankName": "广大音乐",
                 "bankCode": "6213",
                 "unionMark": "0",
                 "type": "debit"
                 })
    print(t.post())
