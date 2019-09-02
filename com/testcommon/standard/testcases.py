# -*- coding: UTF-8 -*-
import logging
import time

from com.common.compareUtil import Compare
from com.service.runjob import Run_job
from com.testcommon.standard.apis.getAsset import GetAsset
from com.testcommon.standard.apis.getCardii import GetCardii
from com.testcommon.standard.apis.getCleanupAmt import GetCleanupAmt
from com.testcommon.standard.apis.getContract import GetContract
from com.testcommon.standard.apis.getOverdueAmt import GetOverdueAmt
from com.testcommon.standard.apis.getRepayPlan import GetRepayPlan
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
        self.bankCard = ""
        self.assetNo = ""
        self.applyAmt = ""
        self.totalTerm = ""
        self.yearRate = ""

    def test_incoming(self):
        try:
            incoming = Incoming()
            result = incoming.post()
            self.certNo = result.get("param").get("data").get("repayer").get("certNo")
            self.mobile = result.get("param").get("data").get("repayer").get("mobile")
            self.name = result.get("param").get("data").get("repayer").get("name")
            self.cardNo = result.get("param").get("data").get("repayCard").get("cardNo")
            self.bankCard = result.get("param").get("data").get("repayCard").get("cardNo")
            self.assetNo = result.get("response").get("data").get("asset_no")
            self.applyAmt = result.get("param").get("data").get("applyAmt")
            self.totalTerm = result.get("param").get("data").get("totalTerm")
            self.yearRate = result.get("param").get("data").get("yearRate")
            self.report.add_result(name="进件测试",
                                   url=result.get("url"),
                                   expect="资产编号非空",
                                   actual=result.get("response"),
                                   param=result.get("param"),
                                   response=result.get("response"),
                                   result=self.compare.str_contains(result.get("response"), "asset_no")
                                   )
        except Exception as e:
            logging.error("资产进件：%s", repr(e))

    def test_get_asset(self):
        try:
            get_asset = GetAsset()
            get_asset.set_filter(certNo=self.certNo, assetNo=self.assetNo)
            result = get_asset.post()
            response = result.get("response")["data"]
            self.report.add_result(name="资产查询",
                                   url=result.get("url"),
                                   expect="期数正确",
                                   actual=response.get("assets")[0].get("totalTerm"),
                                   param=result.get("param"),
                                   response=response,
                                   result=self.compare.equal(self.totalTerm, response.get("assets")[0].get("totalTerm"))
                                   )
            self.report.add_result(name="资产查询",
                                   url=result.get("url"),
                                   expect="日利率正确",
                                   actual=response.get("assets")[0].get("dayRate"),
                                   param=result.get("param"),
                                   response=response,
                                   result=self.compare.equal(float(self.yearRate) / 360,
                                                             response.get("assets")[0].get("dayRate"))
                                   )
            self.report.add_result(name="资产查询",
                                   url=result.get("url"),
                                   expect="申请金额正确",
                                   actual=response.get("assets")[0].get("totalAmt"),
                                   param=result.get("param"),
                                   response=response,
                                   result=self.compare.equal(self.applyAmt, response.get("assets")[0].get("totalAmt"))
                                   )
            i = 0
            while i < 100:
                asset_status = response.get("assets")[0].get("assetStatus")
                if asset_status == "repay":
                    break
                time.sleep(10)
                result = get_asset.post()
                response = result.get("response")["data"]
        except Exception as e:
            logging.error("资产查询：%s", repr(e))

    def test_get_card(self):
        try:
            get_cardii = GetCardii()
            get_cardii.set_filter(certNo=self.certNo)
            result = get_cardii.post()
            response = result.get("response").get("data")
            self.report.add_result(name="查询二类户",
                                   url=result.get("url"),
                                   expect="绑定银行卡正确",
                                   actual=response.get("bind_card")[0].get("card_no"),
                                   param=result.get("param"),
                                   response=response,
                                   result=self.compare.equal(self.bankCard, response.get("bind_card")[0].get("card_no"))
                                   )
            self.report.add_result(name="查询二类户",
                                   url=result.get("url"),
                                   expect="二类户账号正确",
                                   actual=response.get("bind_card")[0].get("card_no"),
                                   param=result.get("param"),
                                   response=response,
                                   result=self.compare.not_equal(None, response.get("bind_card")[0].get("card_no"))
                                   )
        except Exception as e:
            logging.error("查询二类户：%s", repr(e))

    def test_get_contract(self):
        try:
            get_contract = GetContract()
            get_contract.set_filter(self.certNo)
            result = get_contract.post()
            response = result.get("response").get("data")
            self.report.add_result(name="查询合同",
                                   url=result.get("url"),
                                   expect="合同已生成",
                                   actual=response.get("contracts"),
                                   param=result.get("param"),
                                   response=response,
                                   result=self.compare.not_equal(2, len(response.get("contracts")))
                                   )
        except Exception as e:
            logging.error("合同查询：%s", repr(e))

    def test_batch_job(self):
        try:
            run_job = Run_job()
            start_day = run_job.get_core_sys_date()
            result = run_job.run(2)
            end_day = run_job.get_core_sys_date()
            self.report.add_result(name="跑批测试",
                                   url="",
                                   expect="批处理成功",
                                   actual=end_day,
                                   param=start_day,
                                   response=result,
                                   result=self.compare.not_equal(start_day, end_day)
                                   )
        except Exception as e:
            logging.error("批处理测试：%s", repr(e))

    def test_get_repay_plan(self):
        try:
            get_repay_plan = GetRepayPlan()
            get_repay_plan.set_filter(certNo=self.certNo, assetNo=self.assetNo)
            result = get_repay_plan.post()
            response = result.get("response").get("data")
            self.report.add_result(name="查询还款计划",
                                   url=result.get("url"),
                                   expect="还款计划应还总金额正确",
                                   actual=response.get("assets")[0],
                                   param=result.get("param"),
                                   response=response,
                                   result=self.compare.equal(float(self.applyAmt) + float(self.applyAmt) * 2 * 0.0005,
                                                             response.get("total_repay_amt"))
                                   )
        except Exception as e:
            logging.error("查询还款计划：%s", repr(e))

    def test_get_overdue_amt(self):
        try:
            get_overdue_amt = GetOverdueAmt()
            get_overdue_amt.set_filter(certNo=self.certNo, assetNo=self.assetNo)
            result = get_overdue_amt.post()
            response = result.get("response").get("data")
            self.report.add_result(name="查询拖欠金额",
                                   url=result.get("url"),
                                   expect="拖欠金额利息正确",
                                   actual=response.get("assets")[0],
                                   param=result.get("param"),
                                   response=response,
                                   result=self.compare.equal(float(self.applyAmt) + float(self.applyAmt) * 2 * 0.0005,
                                                             response.get("assets")[0].get("repay_int_amt"))
                                   )
        except Exception as e:
            logging.error(repr(e))

    def test_get_cleanup_amt(self):
        try:
            get_cleanup_amp = GetCleanupAmt()
            get_cleanup_amp.set_filter(certNo=self.certNo, assetNo=self.assetNo)
            result = get_cleanup_amp.post()
            response = result.get("response").get("data")
            self.report.add_result(name="查询结清金额",
                                   url=result.get("url"),
                                   expect="结清金额正确",
                                   actual=response.get("assets")[0],
                                   param=result.get("param"),
                                   response=response,
                                   result=self.compare.equal(float(self.applyAmt) + float(self.applyAmt) * 2 * 0.0005,
                                                             response.get("assets")[0].get("cleanup_amt"))
                                   )
        except Exception as e:
            logging.error(repr(e))

if __name__ == '__main__':
    # path = sys.path[0] + "/apis"
    # files = os.listdir(path)
    # os.system("python " + path + "/incoming.py")
    # for file in files:
    #     if str(file).__contains__("incoming") is not True:
    #         print("\n")
    #         print(file,"\n")
    #         os.system("python " + path + "/" + file)
    t = TestCases()
    t.test_incoming()
    t.test_get_asset()
    t.test_get_card()
    t.test_get_contract()
    t.test_batch_job()
    t.test_get_repay_plan()
    t.test_get_overdue_amt()
    t.test_get_cleanup_amt()
