# -*- coding: UTF-8 -*-
import datetime
import logging
import time

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from com.common.redisUtil import Redis
from com.service.model import CoreSysDate


class Run_job:

    def __init__(self):
        self.r = Redis().get_r()
        self.engine = create_engine("mysql+pymysql://tobuser:Ts@2o19_07@172.16.0.7/xy_standard_asset?charset=utf8")
        self.session = sessionmaker(self.engine)
        self.mySession = self.session()
        self.result = self.mySession.query(CoreSysDate)

    def get_core_sys_date(self, project_code):
        return datetime.datetime.strptime(
            str(self.result.filter(CoreSysDate.project_code == project_code).first().core_sys_date),
            "%Y-%m-%d")

    def get_status(self, project_code):
        self.status = self.result.filter(CoreSysDate.project_code == project_code).first().core_sys_status
        return self.status

    def tear_down(self):
        self.session.close_all()

    def write_line(self, line):
        try:
            fp = open("schedule_times.txt", "a+")
            fp.write(line + "\n")
        except:
            pass

    def loadDataSet(self, num, project_code='xy'):
        """
        输入：文件名
        输出：数据集
        描述：从文件读入数据集
        """
        if project_code is None:
            project_code = "xy"
        lock_key = project_code + "_run_status"
        log_key = project_code + "_logs"
        dataSet = self.r.lrange(log_key, 0, 1000)
        return {"logs": dataSet[0:25][::-1], "run_status": self.r.get(lock_key)}

    def run(self, to_date, project_code="xy"):
        try:
            self.lock_key = project_code + "_run_status"
            self.log_key = project_code + "_logs"
            if self.r.get(self.lock_key) == "running":
                return {"message": "正在跑批，请待会重试"}
            else:
                self.r.set(self.lock_key, "running")
            cur_day = self.get_core_sys_date(project_code)
            try:
                end_day = datetime.datetime.strptime(to_date, "%Y-%m-%d")
            except:
                end_day = cur_day + datetime.timedelta(days=int(to_date))
            i = 0
            temp = ""
            log = "跑批至：" + str(end_day)
            self.r.lpush(self.log_key, log)
            logging.info(log)
            while cur_day < end_day:
                cur_day = self.get_core_sys_date(project_code)
                cur_status = self.get_status(project_code)
                if cur_status == "normal" and temp != cur_day:
                    request = requests.post("http://172.16.0.14:8013/start?projectCode=" + project_code)
                    log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " 批处理接口返回：" + request.text
                    self.r.lpush(self.log_key, log)
                    logging.info(log)
                    if request.text != '':
                        self.r.set(self.lock_key, "finish")
                        return {"message": "批处理异常"}
                    log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " 批处理日期：" + str(
                        cur_day.strftime("%Y-%m-%d"))
                    self.r.lpush(self.log_key, log)
                    logging.info(log)
                    temp = cur_day
                    i = 0
                time.sleep(3)
                cur_day = self.get_core_sys_date(project_code)
                cur_status = self.get_status(project_code)
                log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " 查询批处理状态:" + str(
                    cur_day.strftime("%Y-%m-%d")) + " " + cur_status
                self.r.lpush(self.log_key, log)
                logging.info(log)

                i += 1
                if i > 80:
                    break
            log = "跑批结束"
            self.r.lpush(self.log_key, log)
            logging.info(log)
            self.r.set(self.lock_key, "finish")
            self.r.delete("logs")
            return {"message": "跑批完成", "success": True}
        except Exception as e:
            self.r.set(self.lock_key, "finish")
            logging.error(str(e))
            return {"message": "跑批异常", "success": False}
        finally:
            self.tear_down()

    def get_date(self, project_code):
        date = self.get_core_sys_date(project_code).strftime("%Y-%m-%d")
        # self.tear_down()
        return str(date)


if __name__ == "__main__":
    enddate = "20171233"
