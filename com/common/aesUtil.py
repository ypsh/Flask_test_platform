# -*- coding: UTF-8 -*-
import configparser
import logging.config

from Crypto.Cipher import AES

from com.common.getPath import Path


class AesUtil:
    def __init__(self):
        global_path = Path().get_current_path()
        conf = configparser.ConfigParser()
        conf.read(global_path + '/config/config.ini',encoding='utf-8')
        self.secret_key = conf.get('aes_key', 'secret_key')
        self.iv = conf.get('aes_key', 'iv')
        self.data = conf.get('aes_key', 'data')

    # noinspection PyShadowingNames
    def encypt(self, s):
        if s.startswith('xy'):
            return s
        else:
            bs = AES.block_size
            pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
            cipher = AES.new(bytearray(self.secret_key, encoding='utf-8'), AES.MODE_CBC,
                             bytearray(self.iv, encoding='utf-8'))
            msg = cipher.encrypt(bytearray(pad(s), encoding='utf-8'))
            return 'xy' + msg.hex() + self.data

    # noinspection PyShadowingNames
    def decypt(self, s):
        try:
            if s.startswith('xy'):
                s = s[2:s.__len__()]
                s = s[0:-8]
                upad = lambda s: s[0:-ord(s[-1])]
                cipher = AES.new(bytearray(self.secret_key, encoding='utf-8'), AES.MODE_CBC,
                                 bytearray(self.iv, encoding='utf-8'))
                msg = cipher.decrypt(bytes.fromhex(s))
                return upad(str(msg, encoding='utf-8'))
        except Exception as e:
            logging.error(str(e))
            return None

    def aes(self, s):
        s = str(s).replace(" ", "")
        if s.startswith('xy'):
            # result = self.decypt(s)
            return {'result': self.decypt(s)}
        elif s is not '':
            # result = self.encypt(s)
            return {'result': self.encypt(s)}
        else:
            return {'result': '加解密失败'}


if __name__ == '__main__':
    password = 'test'
    password = AesUtil().encypt(password)
    print(password)
    result = AesUtil().decypt(password)
    print(result)
