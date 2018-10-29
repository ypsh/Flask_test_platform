# -*- coding: UTF-8 -*-
import logging

import xlrd


# noinspection PyMethodMayBeStatic
class ExcelOperate:

    def get_excellist(self, file):
        global item
        try:
            result = {}
            workbook = xlrd.open_workbook(file)
            sheet = workbook.sheets()
            if sheet:
                rows = []
                for item in sheet:
                    for i in range(0, item.nrows):
                        temp = []
                        for col in range(0, item.ncols):
                            if item.cell(i, col).ctype == 2:
                                temp.append(str(int(item.cell(i, col).value)))
                            else:
                                temp.append(item.cell(i, col).value)
                        rows.append(temp)
                result[item.name] = rows
                return result
        except Exception as e:
            logging.error(str(e))
            return None
