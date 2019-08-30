# -*- coding: UTF-8 -*-
from com.common.compareUtil import Compare
from com.testcommon.standard.apis.getAsset import GetAsset
from com.testcommon.standard.apis.incoming import Incoming
from com.testcommon.standard.common.testReport import TestReport


class TestCases:
    def __init__(self):
        self.compare = Compare()
        self.report = TestReport()
        self.certNo = ""
        self.name = ""
        self.mobile = ""
        self.cardNo = ""
        self.bankCode = ""
        self.assetNo = ""

    def test_incoming(self):
        try:
            incoming = Incoming()
            result = incoming.post()
            self.report.add_result(name="进件测试",
                                   url=result.get("url"),
                                   expect="资产编号非空",
                                   actual=result.get("response"),
                                   param=result.get("param"),
                                   response=result.get("response"),
                                   result=self.compare.str_contains(result.get("response"), "assert_no")
                                   )
            self.certNo = result.get("param").get("data").get("repayer").get("certNo")
            self.mobile = result.get("param").get("data").get("repayer").get("mobile")
            self.name = result.get("param").get("data").get("repayer").get("name")
            self.cardNo = result.get("param").get("data").get("repayCard").get("cardNo")
            self.bankCode = result.get("param").get("data").get("repayCard").get("bankCode")
            self.assetNo = result.get("response").get("data").get("asset_no")
        except:
            pass

    def test_get_asset(self):
        getasset = GetAsset()
        result = getasset.set_filter(certNo=self.certNo, assetNo=self.assetNo)


if __name__ == '__main__':
    import os, sys

    path = sys.path[0] + "/apis"
    files = os.listdir(path)
    os.system("python " + path + "/incoming.py")
    for file in files:
        if str(file).__contains__("incoming") is not True:
            print("\n")
            print(file,"\n")
            os.system("python " + path + "/" + file)
    # TestCases().test_incoming()
