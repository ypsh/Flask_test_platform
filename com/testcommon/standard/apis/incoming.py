# -*- coding: UTF-8 -*-
import logging
import random
import traceback
from datetime import datetime

import requests

from com.common.generateData import Generate
from com.common.redisUtil import Redis
from com.testcommon.standard.apis.baseApi import BaseApi
from com.testcommon.standard.common.dataDictionary import const


class Incoming(BaseApi):
    url = '/grant/incoming'

    def set_body(self):
        apply_amt = random.randint(10, 1000) * 10000
        total_term = random.randint(1, 4) * 3
        loan_order_no = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(8888, 99999))
        cert_no = Generate().generating_ID_card()
        name = Generate().generating_nanme()
        mobile = Generate().generating_phone_number()
        addr = "四川省成都市天府三街"
        lbs = "四川省太平洋保险金融大厦"
        card_no = Generate().generate_bankcard()
        birth = datetime.strptime(cert_no[6:14], "%Y%m%d").strftime("%Y-%m-%d")
        gender = {0: "M", 1: "F"}[int(cert_no[16]) % 2]
        attachments = [{"hash": "oio283123898d182399dkfv",
                        "name": const.__getrandomvalue__("attachmentsType"),
                        "type": const.__getrandomvalue__("attachmentsType"),
                        "url": "http://test.com"
                        }, {"hash": "oio283123898d182399dkfv",
                            "name": const.__getrandomvalue__("attachmentsType"),
                            "type": const.__getrandomvalue__("attachmentsType"),
                            "url": "http://test.com"
                            }]
        borrower = {"name": name,
                    "certNo": cert_no,
                    "mobile": mobile,
                    "channelCode": "xy-auto_test",
                    "subChannelCode": "xy-channel-sub",
                    "refCode": "ti122",
                    "lbs": lbs,
                    "gender": gender,
                    "nation": const.__getrandomvalue__("nation"),
                    "birth": birth,
                    "addr": addr,
                    "authority": "四川省天府三街公安局",
                    "validFrom": "1999-08-06",
                    "validTo": "2999-08-06",
                    "education": const.__getrandomvalue__("education"),
                    "marriage": const.__getrandomvalue__("marriage"),
                    "addrInfo": {},
                    "contact": [
                        {
                            "addr": addr,
                            "mobile": "18675523992",
                            "name": name + "测试一",
                            "relateType": const.__getrandomvalue__("relateType")
                        },
                        {
                            "addr": addr,
                            "mobile": "18675523992",
                            "name": name + "测试二",
                            "relateType": const.__getrandomvalue__("relateType")
                        }
                    ],
                    "contact_info": [
                        {
                            "info": "kkkkkk",
                            "type": const.__getrandomvalue__("contactType")
                        }
                    ],
                    "thirdInfo": {"third_party": "third_party", "open_id": "open_id"},
                    "workInfo": {
                        "corpName": "公司名称",
                        "corpTel": "07551883162",
                        "corpType": const.__getrandomvalue__("corpType"),
                        "duty": const.__getrandomvalue__("duty"),
                        "industry": const.__getrandomvalue__("industry"),
                        "monthIncome": const.__getrandomvalue__("monthIncome"),
                        "workPlace": "四川省天府三街",
                        "workStatus": const.__getrandomvalue__("workStatus"),
                        "workYear": const.__getrandomvalue__("workYear")
                    }
                    }
        receive_card = {"bankCode": "28283123",
                        "bankName": "中国银行",
                        "cardNo": card_no,
                        "mobile": mobile,
                        "name": name,
                        "type": const.__getrandomvalue__("type"),
                        "unionMark": const.__getrandomvalue__("unionMark")}
        repay_card = receive_card
        repayer = borrower
        data = {"channelCode": "xy channel",
                "subChannelCode": "sub-xy-channel",
                "IntCalcType": const.__getrandomvalue__("intCalcType"),
                "loanUsage": "购物",
                "yearRate": 0.18,
                "callback": "http://119.27.173.43/mock/apis/callback"
                }
        data["productNo"] = self.project_code + "_" + str(random.randint(1, 2))
        data["applyAmt"] = apply_amt
        data["totalTerm"] = total_term
        data["assetNo"] = "AUTO" + loan_order_no
        data["loanOrderNo"] = loan_order_no
        data["attachments"] = attachments
        data["borrower"] = borrower
        data["receiveCard"] = receive_card
        data["repayer"] = repayer
        data["repayCard"] = repay_card
        self.param = data

    def set_cert_no(self, certNO):
        self.cert_no = certNO

    def post(self):
        """
        :return: {"param": self.base_param, "response": self.r.json(), "status": self.r.status_code,"url": self.r.url}
        """
        try:
            self.set_base()
            self.set_body()
            self.set_data()
            b = datetime.now()
            self.r = requests.post(url=self.base_url + self.url, json=self.base_param)
            a = datetime.now()
            self.use_time = (a - b).microseconds / 1000
            key = self.r.json().get("data")
            if key is not None:
                key = key.get("asset_no")
                if key is not None:
                    Redis().set_key(key, self.base_param)
                    Redis().get_r().lpush("assets", key)
            logging.info("请求地址：%s\n请求参数：%s\n响应参数：%s", self.url, self.base_param, self.r.json())
            return {"param": self.base_param, "response": self.r.json(), "status": self.r.status_code,
                    "url": self.r.url, "use_time": self.use_time}
        except Exception as e:
            logging.error("请求报错：%s \n %s", str(traceback.format_exc()), self.r.json())
            return {"param": self.base_param, "response": self.r.json(), "status": self.r.status_code,
                    "url": self.r.url, "use_time": self.use_time}


if __name__ == '__main__':
    import threading


    def run(i, se):
        try:
            se.acquire()
            t = Incoming()
            t.set_project(["xy", "360"][random.randint(0, 1)])
            # t.set_cert_no("522731196408032123")
            result = t.post()
            print(result)

            if result.get("response").get("data").get("asset_no") is None:
                print("失败：%s", result.get("response"))
        except Exception as e:
            print(traceback.format_exc())
        finally:
            se.release()


    r = Redis()
    assets = r.get_list("assets")
    for asset in assets:
        r.delete_key(asset)

    times = 2
    i = 0
    semaphore = threading.BoundedSemaphore(50)
    while i < times:
        t = threading.Thread(target=run, args=(i, semaphore))
        t.start()
        i += 1
        print(i)
