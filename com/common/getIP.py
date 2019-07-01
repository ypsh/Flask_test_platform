# -*- coding: UTF-8 -*-
import csv
import datetime
import os
from com.common.getPath import Path


class SaveIP(object):
    def __init__(self):
        self.path = Path().get_current_path()

    def save(self, ip='', page=''):
        try:
            data = [ip, page, datetime.datetime.now().__format__("%Y-%m-%d %H:%M:%S")]
            file = os.path.join(self.path, "request_ip_info.csv")
            out = open(file, 'a', newline='')
            csv_write = csv.writer(out, dialect='excel')
            csv_write.writerow(data)
        except:
            pass