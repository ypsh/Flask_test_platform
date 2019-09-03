# -*- coding: UTF-8 -*-
import configparser
import logging.config
import time
from datetime import datetime

from com.common.compareUtil import Compare
from com.common.getPath import Path
from com.common.redisUtil import Redis
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
    global_path = Path().get_current_path()
    logging.config.fileConfig(global_path + '/config/logger.conf')
    conf = configparser.ConfigParser()
    conf.read(global_path + '/config/config.ini', encoding='utf-8')
    project_code = "xy"

    def __init__(self):
        self.r = Redis()
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
        self.path = Path().get_current_path()

    def read_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                file_lines = file.readlines()
                return file_lines
        except Exception as e:
            logging.error(repr(e))

    def output_report(self, report):
        try:
            table_data = []
            detail_data = []
            pass_case = 0
            fail_case = 0
            use_time = "10"
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            report_bass_path = self.path + '/com/testcommon/standard/common/report_base.html'
            report_path = self.path + ('/static/standard/report_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.html')
            i = 1
            for case in report:
                case = eval(case)
                table_data.append(
                    [i, case["name"], str(case["expect"]), str(case["actual"]), str(case["result"]),
                     str(case["use_time"])]
                )
                detail_data.append(
                    [i, case["name"], str(case["expect"]), str(case["actual"]), str(case["result"]),
                     str(case["use_time"]), str(case["param"]), str(case["response"]), str(case["url"])])
                if case['result']:
                    pass_case += 1
                else:
                    fail_case += 1
                i += 1

            lines = self.read_file(report_bass_path)
            for i in range(0, len(lines)):
                lines[i] = str(lines[i]).replace('"{{tabledata}}"', str(table_data)).replace('"{{details}}"',
                                                                                             str(detail_data)).replace(
                    '"{{pass}}"', str(pass_case)).replace('"{{fail}}"', str(fail_case)).replace('"{{use_time}}"',
                                                                                                str(use_time)).replace(
                    '"{{create_time}}"', str(create_time))

            with open(report_path, 'w', encoding='utf-8') as f:
                for line in lines:
                    f.write(line)
            logging.info('测试报告生成路径：' + report_path)
        except Exception as e:
            logging.error("生成报告错误：%s", repr(e))

    def test_incoming(self):
        incoming = Incoming()
        incoming.set_project(self.project_code)
        result = incoming.post()
        try:
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
                                   result=self.compare.str_contains(result.get("response"), "asset_no"),
                                   use_time=result.get("use_time")
                                   )
        except Exception as e:
            logging.error("资产进件：%s", repr(e))
            self.report.add_result(name="进件测试",
                                   url=result.get("url"),
                                   actual="进件失败",
                                   result=False,
                                   param=result.get("param"),
                                   response=result.get("response"),
                                   use_time=result.get("use_time")
                                   )

    def test_get_asset(self):
        get_asset = GetAsset()
        get_asset.set_project(self.project_code)
        get_asset.set_filter(certNo=self.certNo, assetNo=self.assetNo)
        result = get_asset.post()
        try:
            response = result.get("response")["data"]
            self.report.add_result(name="资产查询",
                                   url=result.get("url"),
                                   expect="期数正确",
                                   actual=response.get("assets")[0].get("totalTerm"),
                                   param=result.get("param"),
                                   response=response,
                                   use_time=result.get("use_time"),
                                   result=self.compare.equal(self.totalTerm, response.get("assets")[0].get("totalTerm"))
                                   )
            self.report.add_result(name="资产查询",
                                   url=result.get("url"),
                                   expect="日利率正确",
                                   actual=response.get("assets")[0].get("dayRate"),
                                   param=result.get("param"),
                                   response=response,
                                   use_time=result.get("use_time"),
                                   result=self.compare.equal(float(self.yearRate) / 360,
                                                             response.get("assets")[0].get("dayRate"))
                                   )
            self.report.add_result(name="资产查询",
                                   url=result.get("url"),
                                   expect="申请金额正确",
                                   actual=response.get("assets")[0].get("totalAmt"),
                                   param=result.get("param"),
                                   response=response,
                                   use_time=result.get("use_time"),
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
            self.report.add_result(name="资产查询",
                                   url=result.get("url"),
                                   actual="资产查询失败",
                                   result=False,
                                   param=result.get("param"),
                                   response=result.get("response"),
                                   use_time=result.get("use_time")
                                   )

    def test_get_card(self):
        get_cardii = GetCardii()
        get_cardii.set_project(self.project_code)
        get_cardii.set_filter(certNo=self.certNo)
        result = get_cardii.post()
        try:
            response = result.get("response").get("data")
            self.report.add_result(name="查询二类户",
                                   url=result.get("url"),
                                   expect="绑定银行卡正确",
                                   actual=response.get("bind_card")[0].get("card_no"),
                                   param=result.get("param"),
                                   response=response,
                                   use_time=result.get("use_time"),
                                   result=self.compare.equal(self.bankCard, response.get("bind_card")[0].get("card_no"))
                                   )
            self.report.add_result(name="查询二类户",
                                   url=result.get("url"),
                                   expect="二类户账号正确",
                                   actual=response.get("bind_card")[0].get("card_no"),
                                   param=result.get("param"),
                                   response=response,
                                   use_time=result.get("use_time"),
                                   result=self.compare.not_equal(None, response.get("bind_card")[0].get("card_no"))
                                   )
        except Exception as e:
            logging.error("查询二类户：%s", repr(e))
            self.report.add_result(name="查询二类户",
                                   url=result.get("url"),
                                   actual="查询二类户失败",
                                   result=False,
                                   param=result.get("param"),
                                   response=result.get("response"),
                                   use_time=result.get("use_time")
                                   )

    def test_get_contract(self):
        get_contract = GetContract()
        get_contract.set_project(self.project_code)
        get_contract.set_filter(self.assetNo)
        result = get_contract.post()
        try:
            response = result.get("response").get("data")
            self.report.add_result(name="查询合同",
                                   url=result.get("url"),
                                   expect="合同已生成",
                                   actual=response.get("contracts"),
                                   param=result.get("param"),
                                   response=response,
                                   use_time=result.get("use_time"),
                                   result=self.compare.equal(2, len(response.get("contracts")))
                                   )
        except Exception as e:
            logging.error("合同查询：%s", repr(e))
            self.report.add_result(name="合同查询",
                                   url=result.get("url"),
                                   actual="合同查询失败",
                                   result=False,
                                   param=result.get("param"),
                                   response=result.get("response"),
                                   use_time=result.get("use_time")
                                   )

    def test_batch_job(self):
        try:
            run_job = Run_job()
            start_day = run_job.get_core_sys_date(project_code=self.project_code)
            result = run_job.run(to_date=2, project_code=self.project_code)
            end_day = run_job.get_core_sys_date(project_code=self.project_code)
            self.report.add_result(name="跑批测试",
                                   url="",
                                   expect="批处理成功",
                                   actual=str(end_day),
                                   param=str(start_day),
                                   response=result,
                                   result=self.compare.not_equal(start_day, end_day)
                                   )
        except Exception as e:
            logging.error("批处理测试：%s", repr(e))

    def test_get_repay_plan(self):
        get_repay_plan = GetRepayPlan()
        get_repay_plan.set_project(self.project_code)
        get_repay_plan.set_filter(certNo=self.certNo, assetNo=self.assetNo)
        result = get_repay_plan.post()
        try:
            response = result.get("response").get("data")
            self.report.add_result(name="查询还款计划",
                                   url=result.get("url"),
                                   expect="还款计划应还总金额正确",
                                   actual=response.get("assets")[0],
                                   param=result.get("param"),
                                   response=response,
                                   use_time=result.get("use_time"),
                                   result=self.compare.equal(float(self.applyAmt) + float(self.applyAmt) * 2 * 0.0005,
                                                             response.get("total_repay_amt"))
                                   )
        except Exception as e:
            logging.error("查询还款计划：%s", repr(e))
            self.report.add_result(name="查询还款计划",
                                   url=result.get("url"),
                                   actual="查询还款计划失败",
                                   result=False,
                                   param=result.get("param"),
                                   response=result.get("response"),
                                   use_time=result.get("use_time")
                                   )

    def test_get_overdue_amt(self):
        get_overdue_amt = GetOverdueAmt()
        get_overdue_amt.set_project(self.project_code)
        get_overdue_amt.set_filter(certNo=self.certNo, assetNo=self.assetNo)
        result = get_overdue_amt.post()
        try:
            response = result.get("response").get("data")
            self.report.add_result(name="查询拖欠金额",
                                   url=result.get("url"),
                                   expect="拖欠金额利息正确" + str(float(self.applyAmt) * 2 * 0.0005),
                                   actual=response.get("assets")[0],
                                   param=result.get("param"),
                                   response=response,
                                   use_time=result.get("use_time"),
                                   result=self.compare.equal(float(self.applyAmt) * 2 * 0.0005,
                                                             response.get("assets")[0].get("repay_int_amt"))
                                   )
        except Exception as e:
            logging.error(repr(e))
            self.report.add_result(name="查询拖欠金额",
                                   url=result.get("url"),
                                   actual="查询拖欠金额失败",
                                   result=False,
                                   param=result.get("param"),
                                   response=result.get("response"),
                                   use_time=result.get("use_time")
                                   )

    def test_get_cleanup_amt(self):
        get_cleanup_amp = GetCleanupAmt()
        get_cleanup_amp.set_project(self.project_code)
        get_cleanup_amp.set_filter(certNo=self.certNo, assetNo=self.assetNo)
        result = get_cleanup_amp.post()
        try:
            response = result.get("response").get("data")
            self.report.add_result(name="查询结清金额",
                                   url=result.get("url"),
                                   expect="结清金额正确",
                                   actual=response.get("assets")[0],
                                   param=result.get("param"),
                                   response=response,
                                   use_time=result.get("use_time"),
                                   result=self.compare.equal(float(self.applyAmt) + float(self.applyAmt) * 2 * 0.0005,
                                                             response.get("assets")[0].get("cleanup_amt"))
                                   )
        except Exception as e:
            logging.error(repr(e))
            self.report.add_result(name="查询结清金额",
                                   url=result.get("url"),
                                   actual="查询结清金额失败",
                                   result=False,
                                   param=result.get("param"),
                                   response=result.get("response"),
                                   use_time=result.get("use_time")
                                   )

    def run_test(self, project_code=None):
        try:
            if project_code is not None:
                self.project_code = project_code
            smoking_status = self.r.get_key("smoking_status")
            if smoking_status != "running":
                self.r.set_key("smoking_status", "running")
            else:
                return {"sucess": True, "message": "冒烟测试中"}
            assets = self.r.get_list("assets")
            for asset in assets:
                self.r.delete_key(asset)
            self.r.delete_key("assets")
            self.r.delete_key("test_result")
            self.test_incoming()
            self.test_get_asset()
            self.test_get_card()
            self.test_batch_job()
            self.test_get_repay_plan()
            self.test_get_overdue_amt()
            self.test_get_cleanup_amt()
            self.test_get_contract()
            report = self.r.get_list("test_result")
            self.output_report(report)
            return {"sucess": True, "message": "跑批完成"}
        except:
            return {"sucess": False, "message": "冒烟测试中"}
        finally:
            self.r.set_key("smoking_status", "finish")

    def get_status(self):
        return self.r.get_key("smoking_status")


if __name__ == '__main__':
    # path = sys.path[0] + "/apis"
    # files = os.listdir(path)
    # os.system("python " + path + "/incoming.py")
    # for file in files:
    #     if str(file).__contains__("incoming") is not True:
    #         print("\n")
    #         print(file,"\n")
    #         os.system("python " + path + "/" + file)
    # 创建一个logger
    t = TestCases()
    t.run_test("360")
