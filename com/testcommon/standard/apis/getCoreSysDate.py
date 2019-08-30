# -*- coding: UTF-8 -*-

from com.testcommon.standard.apis.baseApi import BaseApi


class GetCoreSysDate(BaseApi):
    url = '/core/get-core-sys-date'


if __name__ == '__main__':
    t = GetCoreSysDate()
    print(t.post())
