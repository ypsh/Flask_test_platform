# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class CardiiWithdraw(BaseApi):
    url = '/cardii/withdraw'
    data = {}
    param = data

    def set_param(self, **kwargs):
        """
        :param kwargs: certNo amount receiverName receiverCardNo receiverBankName receiverBankCode
        :return:
        """
        self.data["certNo"] = kwargs.get("certNo")
        self.data["amount"] = kwargs.get("amount")
        self.data["receiverName"] = kwargs.get("receiverName")
        self.data["receiverCardNo"] = kwargs.get("receiverCardNo")
        self.data["receiverBankName"] = kwargs.get("receiverBankName")
        self.data["receiverBankCode"] = kwargs.get("receiverBankCode")


if __name__ == '__main__':
    t = CardiiWithdraw()
    t.set_param(certNo="522731196408032123",
                amount=200,
                receiverName="广盛",
                receiverBankCode=28283123,
                receiverCardNo="6228446728592785943",
                receiverBankName="中国银行"
                )
    print(t.post())
