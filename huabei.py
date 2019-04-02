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
    dates = ['20180602', '20180603', '20180604', '20180605', '20180606', '20180607', '20180608', '20180609', '20180610',
             '20180611', '20180612', '20180613', '20180614', '20180615', '20180616', '20180617', '20180618', '20180619',
             '20180620', '20180621', '20180622', '20180623', '20180624', '20180625', '20180626', '20180627', '20180628',
             '20180629', '20180630', '20180701', '20180702', '20180703', '20180704', '20180705', '20180706', '20180707',
             '20180708', '20180709', '20180710', '20180711', '20180712', '20180713', '20180714', '20180715', '20180716',
             '20180717', '20180718', '20180719', '20180720', '20180721', '20180722', '20180723', '20180724', '20180725',
             '20180726', '20180727', '20180728', '20180729', '20180730', '20180731', '20180801', '20180802', '20180803',
             '20180804', '20180805', '20180806', '20180807', '20180808', '20180809', '20180810', '20180811', '20180812',
             '20180813', '20180814', '20180815', '20180816', '20180817', '20180818', '20180819', '20180820', '20180821',
             '20180822', '20180823', '20180824', '20180825', '20180826', '20180827', '20180828', '20180829', '20180830',
             '20180831', '20180901', '20180902', '20180903', '20180904', '20180905', '20180906', '20180907', '20180908',
             '20180909', '20180910', '20180911', '20180912', '20180913', '20180914', '20180915', '20180916', '20180917',
             '20180918', '20180919', '20180920', '20180921', '20180922', '20180923']

    print(dates)
    h.run(dates)
