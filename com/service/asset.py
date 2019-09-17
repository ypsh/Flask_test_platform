# -*- coding: UTF-8 -*-
import configparser
import datetime
import json
import logging
import time
import traceback
from datetime import date
from datetime import datetime

import gevent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from com.common.getPath import Path
from com.common.redisUtil import Redis
from com.service.model import CoreSysDate
from com.testcommon.standard.apis.incoming import Incoming


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class Asset:
    def __init__(self):
        self.path = Path().get_current_path()
        conf = configparser.ConfigParser()
        conf.read(self.path + '/config/config.ini', encoding='utf-8')
        self.mysql = conf.get('server', 'mysql')
        self.r = Redis().get_r()
        self.engine = create_engine(self.mysql + "/?charset=utf8")
        self.session = sessionmaker(self.engine)
        self.mySession = self.session()
        self.result = self.mySession.query(CoreSysDate)

    def get_assets(self, asset_no):
        if asset_no != "":
            sql = """SELECT asset_id,asset_no,project_code,prin_amt,total_term,int_calc_type,asset_status,create_time 
                FROM xy_standard_asset.asset where asset_no="???" """
            sql = sql.replace("???", asset_no)
            result = self.mySession.execute(sql)
        else:
            result = self.mySession.execute(
                """SELECT asset_id,asset_no,project_code,prin_amt,total_term,int_calc_type,asset_status,create_time 
                FROM xy_standard_asset.asset ORDER BY asset_id DESC LIMIT 100""")
        return json.dumps(result._saved_cursor._result.rows, cls=ComplexEncoder)

    def get_info(self, asst_no):
        sql = """
        SELECT a.asset_no, a.project_code,  individual.name, individual.cert_no, cardii.card_no AS cardii_no, cardi.card_no AS cardi_no, account.acct_id, individual.mobile,cardi.status
FROM xy_standard_asset.asset a, xy_standard_account.account account, xy_standard_account.cardii cardii, xy_standard_account.cardi cardi , 
xy_standard_account.cust cust, xy_standard_account.individual individual
WHERE a.repayer = account.acct_id
AND account.cust_id = cust.cust_id
AND account.acct_id = cardi.acct_id
AND cardii.acct_id = account.acct_id
AND cust.cust_id = individual.cust_id
AND a.asset_no = "@@@@@@" LIMIT 1
        """
        sql = sql.replace("@@@@@@", str(asst_no))
        result = self.mySession.execute(sql)
        data = result._saved_cursor._result.rows
        return {"data": {"name": data[0][2],
                         "cardiiNo": data[0][4],
                         "cardNo": data[0][5],
                         "mobile": data[0][7],
                         "payAccount": data[0][4],
                         "repayName": data[0][2],
                         "certNo": data[0][3],
                         "assetNo": data[0][0]
                         }}

    def incomming(self, project_code, num, totalterm=None, intcaltype=None):
        def run(i, project_code, totalterm, intcaltype):
            try:
                # se.acquire()
                t = Incoming()
                t.set_project(project_code)
                # t.set_cert_no("522731196408032123")
                result = t.post(totalterm, intcaltype)
                logging.info("耗时：%s", result["use_time"])
                logging.info(result)
                # print(result)

                if result.get("response").get("data").get("asset_no") is None:
                    logging.info("失败：%s", result.get("response"))
            except Exception as e:
                logging.error(traceback.format_exc())
            # finally:
            #     se.release()

        r = Redis()
        assets = r.get_list("assets")
        for asset in assets:
            r.delete_key(asset)

        # times = num
        # i = 0
        # semaphore = threading.BoundedSemaphore(5)
        # while i < times:
        #     t = threading.Thread(target=run, args=(i, semaphore, project_code, totalterm, intcaltype))
        #     t.start()
        #     i += 1

        begin_time = time.time()
        run_gevent_list = []
        for i in range(num):
            logging.info('--------------%d--Test-------------' % i)
            run_gevent_list.append(gevent.spawn(run(i, project_code, totalterm, intcaltype)))
        gevent.joinall(run_gevent_list)
        end = time.time()
        print('单次测试时间（平均）s:', (end - begin_time) / num)
        print('累计测试时间 s:', end - begin_time)
        return {"sucess": True}


if __name__ == '__main__':
    # print(Asset().get_assets())
    Asset().incomming("xy", 2)
