# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class VoluntaryRepay(BaseApi):
    url = '/repay/voluntary-repay'
    data = {}
    param = data

    def set_param(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        self.data["certNo"] = kwargs.get("certNo")
        self.data["payChannel"] = kwargs.get("payChannel")
        self.data["repayAmt"] = kwargs.get("repayAmt")
        self.data["repayType"] = kwargs.get("repayType")
        self.data["cardNo"] = kwargs.get("cardNo")
        self.data["repayName"] = kwargs.get("repayName")
        self.data["couponNo"] = kwargs.get("couponNo")
        self.data["couponAmt"] = kwargs.get("couponAmt")
        self.data["assets"] = kwargs.get("assets")


if __name__ == '__main__':
    t = VoluntaryRepay()
    t.set_param(certNo="522731196408032123",
                payChannel="cardii",
                repayAmt="200",
                repayType="term",
                cardNo="62190827096523439",
                repayName="广盛",
                couponNo="",
                couponAmt="500",
                assets={"asset_no": "A201908141544346624682"}
                )
    print(t.post())
