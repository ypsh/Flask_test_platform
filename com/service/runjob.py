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
        self.engine = create_engine("mysql+pymysql://tobuser:ts@123@172.16.0.13/xy_standard_asset?charset=utf8")
        self.session = sessionmaker(self.engine)
        self.mySession = self.session()
        self.result = self.mySession.query(CoreSysDate)

    def get_core_sys_date(self,project_code):
        return datetime.datetime.strptime(
            str(self.result.filter(CoreSysDate.project_code == project_code).first().core_sys_date),
            "%Y-%m-%d")

    def get_status(self,project_code):
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

    def loadDataSet(self, line, splitChar="\t"):
        """
        输入：文件名
        输出：数据集
        描述：从文件读入数据集
        """
        # fileName = "schedule_times.txt"
        # file = os.path.join(Path().get_current_path() + "/logs", "myapp.log")
        # dataSet = []
        # with open(file) as fr:
        #     for line in fr.readlines()[-200:]:
        #         if str(line).find("runjob") != -1:
        #             dataSet.append(line)
        dataSet = self.r.lrange("logs", 0, 1000)
        return {"logs": dataSet[0:14][::-1], "run_status": self.r.get("run_status")}

    def run(self, to_date, project_code="xy"):
        try:
            if self.r.get("run_status") == "running":
                return {"message": "正在跑批，请待会重试"}
            else:
                self.r.set("run_status", "running")
            cur_day = self.get_core_sys_date(project_code)
            try:
                end_day = datetime.datetime.strptime(to_date, "%Y-%m-%d")
            except:
                end_day = cur_day + datetime.timedelta(days=int(to_date))
            i = 0
            temp = ""
            log = "跑批至：" + str(end_day)
            self.r.lpush("logs", log)
            logging.info(log)
            while cur_day < end_day:
                cur_day = self.get_core_sys_date(project_code)
                cur_status = self.get_status(project_code)
                if cur_status == "normal" and temp != cur_day:
                    request = requests.post("http://172.16.0.13:8013/start?projectCode=" + project_code)
                    log = "批处理日期：" + str(cur_day.strftime("%Y-%m-%d"))
                    self.r.lpush("logs", log)
                    logging.info(log)
                    temp = cur_day
                    i = 0
                time.sleep(3)
                cur_day = self.get_core_sys_date(project_code)
                cur_status = self.get_status(project_code)
                log = "查询批处理状态:" + str(cur_day) + cur_status
                self.r.lpush("logs", log)
                logging.info(log)

                i += 1
                if i > 80:
                    break
            log = "跑批结束"
            self.r.lpush("logs", log)
            logging.info(log)
            self.r.set("run_status", "finish")
            self.r.delete("logs")
            return {"message": "跑批完成", "success": True}
        except Exception as e:
            self.r.set("run_status", "finish")
            logging.error(str(e))
            return {"message": "跑批异常", "success": False}
        finally:
            self.tear_down()

    def get_date(self,project_code):
        date = self.get_core_sys_date(project_code).strftime("%Y-%m-%d")
        # self.tear_down()
        return str(date)


if __name__ == "__main__":
    enddate = "20171233"
