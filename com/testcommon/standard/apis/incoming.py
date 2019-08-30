# -*- coding: UTF-8 -*-
import logging
import random
from datetime import datetime

import requests

from com.common.generateData import Generate
from com.common.redisUtil import Redis
from com.testcommon.standard.apis.baseApi import BaseApi
from com.testcommon.standard.common.dataDictionary import const


class Incoming(BaseApi):
    url = '/grant/incoming'
    apply_amt = random.randint(10, 1000) * 10000
    total_term = random.randint(1, 4) * 3
    loan_order_no = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(0, 9999))
    cert_no = Generate().generating_ID_card()
    name = Generate().generating_nanme()
    mobile = Generate().generating_phone_number()
    addr = "四川省成都市天府三街"
    lbs = "四川省太平洋保险金融大厦"
    card_no = Generate().generate_bankcard()
    birth = datetime.strptime(cert_no[6:14], "%Y%m%d").strftime("%Y-%m-%d")
    gender = {0: "M", 1: "F"}[int(cert_no[16]) % 2]
    attachments = [{"hash": "oio283123898d182399dkfv",
                    "name": const.__getrandomvalue__("attachments_type"),
                    "type": const.__getrandomvalue__("attachments_type"),
                    "url": "http://test.com"
                    }, {"hash": "oio283123898d182399dkfv",
                        "name": const.__getrandomvalue__("attachments_type"),
                        "type": const.__getrandomvalue__("attachments_type"),
                        "url": "http://test.com"
                        }]
    borrower = {"name": name,
                "cert_no": cert_no,
                "mobile": mobile,
                "channel_code": "xy-auto_test",
                "sub_channel_code": "xy-channel-sub",
                "ref_code": "ti122",
                "lbs": lbs,
                "gender": gender,
                "nation": const.__getrandomvalue__("nation"),
                "birth": birth,
                "addr": addr,
                "authority": "四川省天府三街公安局",
                "valid_from": "1999-08-06",
                "valid_to": "2999-08-06",
                "education": const.__getrandomvalue__("education"),
                "marriage": const.__getrandomvalue__("marriage"),
                "addr_info": {},
                "contact": [
                    {
                        "addr": addr,
                        "mobile": "18675523992",
                        "name": name + "测试一",
                        "relate_type": const.__getrandomvalue__("relate_type")
                    },
                    {
                        "addr": addr,
                        "mobile": "18675523992",
                        "name": name + "测试二",
                        "relate_type": const.__getrandomvalue__("relate_type")
                    }
                ],
                "contact_info": [
                    {
                        "info": "kkkkkk",
                        "type": const.__getrandomvalue__("contact_type")
                    }
                ],
                "third_info": {"third_party": "third_party", "open_id": "open_id"},
                "work_info": {
                    "corp_name": "公司名称",
                    "corp_tel": "07551883162",
                    "corp_type": const.__getrandomvalue__("corp_type"),
                    "duty": const.__getrandomvalue__("duty"),
                    "industry": const.__getrandomvalue__("industry"),
                    "month_income": const.__getrandomvalue__("month_income"),
                    "work_place": "四川省天府三街",
                    "work_status": const.__getrandomvalue__("work_status"),
                    "work_year": const.__getrandomvalue__("work_year")
                }
                }
    receive_card = {"bank_code": "28283123",
                    "bank_name": "中国银行",
                    "card_no": card_no,
                    "mobile": mobile,
                    "name": name,
                    "type": const.__getrandomvalue__("type"),
                    "union_mark": const.__getrandomvalue__("union_mark")}
    repay_card = receive_card
    repayer = borrower
    data = {"channel_code": "xy channel",
            "sub_channel_code": "sub-xy-channel",
            "loan_order_no": loan_order_no,
            "product_no": "xy_1",
            "int_calc_type": "eq_prin_int",
            "total_term": 12,
            "loan_usage": "购物",
            "year_rate": 0.18,
            "apply_amt": 500000,
            "callback": "http://119.27.173.43/mock/apis/callback"
            }
    data["applyAmt"] = apply_amt
    data["totalTerm"] = total_term
    data["loanOrderNo"] = loan_order_no
    data["attachments"] = attachments
    data["borrower"] = borrower
    data["receiveCard"] = receive_card
    data["repayer"] = repayer
    data["repayCard"] = repay_card
    param = data

    def set_cert_no(self,certNO):
        self.cert_no=certNO

    def post(self):
        """
        :return: {"param": self.base_param, "response": self.r.json(), "status": self.r.status_code,"url": self.r.url}
        """
        try:
            self.set_data()
            self.r = requests.post(url=self.base_url + self.url, json=self.base_param)
            key = self.r.json().get("data")
            if key is not None:
                key = key.get("asset_no")
                if key is None:
                    Redis().set_key(key, self.base_param)
                    Redis().get_r().lpush("assets", key)
            return {"param": self.base_param, "response": self.r.json(), "status": self.r.status_code,
                    "url": self.r.url}
        except Exception as e:
            logging.error("请求报错：%s \n %s", repr(e), self.r.json())
            return {"param": self.base_param, "response": self.r.json(), "status": self.r.status_code,
                    "url": self.r.url}


if __name__ == '__main__':
    t = Incoming()
    t.set_cert_no("522731196408032123")
    print(t.post())
