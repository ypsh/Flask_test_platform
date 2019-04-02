# -*- coding: UTF-8 -*-

import os
import time

import requests

import pymysql as pymysql


class huabei:
    def set_up_huabei(self):
        self.db = pymysql.connect("172.16.100.128", "tobuser", "ts@123", "db_huabei")
        self.cursor = self.db.cursor()

    def tear_down(self):
        self.db.close()

    def get_all_date(self, path):
        return os.listdir(path)

    def get_coredate_huabei(self):
        try:
            self.cursor.execute("select * from core_sys_date where asset_type = 'huabei'")
            data = self.cursor.fetchall()
            if data[0][3] == 'running':
                return data[0][2]
            else:
                return None
        except Exception as e:
            print(str(e))

    def updata_core_date(self, date):
        sql = "update core_sys_date set core_sys_date = '" + str(date) + "' where asset_type = 'huabei'"
        self.cursor.execute(sql)
        self.db.commit()

    def run(self, dates):
        try:
            # dates = self.get_all_date()
            self.set_up_huabei()
            for i in range(0, len(dates)):
                date = dates[i]
                core_date = self.get_coredate_huabei()
                task = requests.get(
                    'http://172.16.100.125:8091/huabei-test/start/huabei')
                if task.text.__contains__('OK'):
                    pass
                else:
                    return False
                run_task = requests.get('http://172.16.100.125:8091/huabei-test/startjob')
                core_now = self.get_coredate_huabei()
                while core_date == core_now:
                    time.sleep(1)
                    core_now = self.get_coredate_huabei()
                    # print('等待任务结束')
                    run_task = requests.get('http://172.16.100.125:8091/huabei-test/startjob')
                self.updata_core_date(dates[i + 1])
                print(dates[i + 1])
        except Exception as e:
            print(str(e))
        finally:
            self.tear_down()


if __name__ == '__main__':
    h = huabei()
    # dates = h.get_all_date('new')[1:]
    dates = ['20180602', '20180603', '20180604', '20180605', '20180606', '20180607', '20180608', '20180609', '20180610']

    print(dates)
    h.run(dates)
