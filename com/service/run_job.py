import datetime
import json
import os

import paramiko as paramiko
import pymysql
import logging

import requests

from com.common.getPath import Path


class Run_job:

    def set_up(self):
        self.db = pymysql.connect("172.16.100.128", "tobuser", "ts@123", "db_biz")
        self.cursor = self.db.cursor()

    def get_coredate(self):
        try:
            self.cursor.execute("select * from core_sys_date where asset_type = 'jnb_haoyidai'")
            data = self.cursor.fetchall()
            if data[0][3] == 'running':
                return data[0][2]
            else:
                return None
        except Exception as e:
            logging.error(str(e))

    def run_batchjob(self, date):
        try:
            run = requests.get(
                'http://172.16.100.125:8088/batchjob/startDayendBatchJob?assetType=jnb_haoyidai&toDate=%s' % date)
            logging.info("跑批完成%s" % date)
            accrual = requests.get('http://172.16.100.125:8087/report/genDailyData?assetType=jnb_haoyidai')
            runreport = json.dumps(accrual.json())
            lastreport = json.loads(runreport)
            if lastreport.get('message') == 'success':
                sql = "update core_sys_date set core_sys_date = '" + str(date) + "' where asset_type = 'jnb_haoyidai'"
                self.cursor.execute(sql)
                self.db.commit()
                logging.info("生成报表完成%s" % date)
            return True
        except Exception as e:
            logging.error(str(e))
            return False

    def tear_down(self):
        self.db.close()

    def write_line(self, line):
        try:
            fp = open('schedule_times.txt', 'a+')
            fp.write(line + '\n')
        except:
            pass

    def loadDataSet(self, line, splitChar='\t'):
        """
        输入：文件名
        输出：数据集
        描述：从文件读入数据集
        """
        fileName = 'schedule_times.txt'
        file = os.path.join(Path().get_current_path(), 'myapp.log')
        dataSet = []
        with open(file) as fr:
            for line in fr.readlines()[-200:]:
                if str(line).find('runjob') == -1:
                    dataSet.append(line)
        return dataSet[-14:]

    def run(self, enddate):
        try:
            self.set_up()
            codedate = self.get_coredate()
            # codedate = '2019-04-28'
            datesart = datetime.datetime.strptime(str(codedate), '%Y-%m-%d')
            dateend = datetime.datetime.strptime(enddate, '%Y-%m-%d')
            if dateend <= datesart:
                return {'message': '结束时间小于开始时间', 'date': str(datesart)}
            else:
                while datesart < dateend:
                    datesart += datetime.timedelta(days=1)
                    self.run_batchjob(str(datesart).split(' ')[0])
                    self.run_ssh()
                return {'message': '跑批结束，当前日期%s' % str(datesart), 'date': str(datesart)}
        except Exception as e:
            logging.error(str(e))
        finally:
            self.tear_down()

    def get_date(self):
        self.set_up()
        date = self.get_coredate()
        self.tear_down()
        return date

    """
    #放款统计任务
    /usr/bin/php /data/bank/jnpaydayloan/yii statistics/grant-stat/init
    /usr/bin/php /data/bank/jnpaydayloan/yii statistics/grant-stat/update-status
    #风控进件统计任务
    /usr/bin/php /data/bank/jnpaydayloan/yii v1/individual-verify/init-verify
    /usr/bin/php /data/bank/jnpaydayloan/yii v1/individual-verify/update-exception-verify
    /usr/bin/php /data/bank/jnpaydayloan/yii v1/individual-verify/init-apply
    /usr/bin/php /data/bank/jnpaydayloan/yii v1/individual-verify/update-exception-apply
    #每日资产逾期更新
    /usr/bin/php /data/bank/jnpaydayloan/yii statistics/grant-stat/update
    #账龄MOB统计
    /usr/bin/php /data/bank/jnpaydayloan/yii statistics/grant-stat-by-cycle/init
    #催回率统计
    /usr/bin/php /data/bank/jnpaydayloan/yii statistics/repay-plan-by-cycle/init
    这些会每5分钟执行一次
    """

    def run_ssh(self):
        try:
            list = [
                '/usr/bin/php /data/bank/jnpaydayloan/yii statistics/grant-stat/init',
                '/usr/bin/php /data/bank/jnpaydayloan/yii statistics/grant-stat/update-status',
                '/usr/bin/php /data/bank/jnpaydayloan/yii v1/individual-verify/init-verify',
                '/usr/bin/php /data/bank/jnpaydayloan/yii v1/individual-verify/update-exception-verify',
                '/usr/bin/php /data/bank/jnpaydayloan/yii v1/individual-verify/init-apply',
                '/usr/bin/php /data/bank/jnpaydayloan/yii v1/individual-verify/update-exception-apply',
                '/usr/bin/php /data/bank/jnpaydayloan/yii statistics/grant-stat/update',
                '/usr/bin/php /data/bank/jnpaydayloan/yii statistics/grant-stat-by-cycle/init',
                '/usr/bin/php /data/bank/jnpaydayloan/yii statistics/repay-plan-by-cycle/init'
            ]
            # 创建SSH对象
            ssh = paramiko.SSHClient()
            # 允许连接不在know_hosts文件中的主机
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            ssh.connect(hostname='172.16.100.126', port=22, username='mng', password='Bsd4#df23$ffVq!md')
            # 执行命令
            for item in list:
                stdin, stdout, stderr = ssh.exec_command(item)
                # 获取命令结果
                result = stdout.read()
                logging.info(item)
                logging.info(result)
        except Exception as e:
            logging.error(str(e))
        finally:
            ssh.close()


if __name__ == '__main__':
    Run_job().run_ssh()
