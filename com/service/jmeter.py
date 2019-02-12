import datetime
import logging
import os
import sys

from com.common.getPath import Path


class Jmeter:
    def __init__(self):
        self.globalpath = Path().get_current_path()

    """
    查找jmeter 目录
    """

    def find_jmeter(self, path):
        try:
            result = None
            files = os.listdir(path)
            for fi in files:
                fi_d = os.path.join(path, fi)
                if os.path.isdir(fi_d):
                    result = self.find_jmeter(fi_d)
                    if result:
                        break
                else:
                    if fi == 'jmeter':
                        result = fi_d
                        break
            return result
        except Exception as e:
            logging.error(str(e))

    """
    创建报告目录
    """

    def make_dir(self, jmx):
        try:
            jmx = jmx.split('.')[0]
            dir_name = jmx + "_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            path = os.path.join(self.globalpath, 'static')
            report = os.path.join(path,'report')
            if os.path.exists(report):
                pass
            else:
                os.mkdir(report)
            path=os.path.join(path,'report')
            dir_path = os.path.join(path, dir_name)
            if os.path.exists(dir_path) is not True:
                os.mkdir(dir_path)
                return dir_path
            else:
                return None
        except Exception as e:
            logging.error("创建报告目录失败" + str(e))

    def execute_jmx(self, jmx):
        try:
            path = os.path.join(self.globalpath, 'jmeter')
            reportpath = self.make_dir(jmx)
            jmxpath = os.path.join(path, 'jmx', jmx)
            jtlpath = os.path.join(reportpath, 'result.jtl')
            resultpath = os.path.join(reportpath, 'result')
            logpath = os.path.join(reportpath, 'jmeter.log')
            command = self.find_jmeter(
                path) + " -n -t " + jmxpath + ' -l ' + jtlpath + " -e -o " + resultpath + " -j " + logpath
            os.popen(command)
            return {'message':True}
        except Exception as e:
            return {'message':False}


if __name__ == '__main__':
    path = Path().get_current_path() + '/jmeter'
    Jmeter().execute_jmx('秦农-查询.jmx')
