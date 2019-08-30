# -*-coding:utf-8-*-
import configparser
import logging
import logging.config

import redis
from rediscluster import StrictRedisCluster

from com.common.getPath import Path

'''
redis 配置
'''


class Redis:
    global_path = Path().get_current_path()
    password = ''

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379,
                             decode_responses=True)  # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379

    def get_nodes(self):
        nodes = []
        try:
            conf = configparser.ConfigParser()
            conf.read(self.global_path + '/config/config.ini', encoding='utf-8')
            host_port = conf.get('redis', 'nodes')
            ips = host_port.split(',')
            self.password = conf.get('redis', 'password')
            for item in ips:
                m = {'host': item.split(':')[0], 'port': item.split(':')[1]}
                nodes.append(m)
            logging.info('nodes:%s' % nodes)
        except Exception as e:
            logging.error(str(e))
        return nodes

    def config_redis(self):
        revisions = None
        redis_nodes = self.get_nodes()
        try:
            if self.password == "":
                revisions = StrictRedisCluster(startup_nodes=redis_nodes)
            else:
                revisions = StrictRedisCluster(startup_nodes=redis_nodes, password=self.password)
        except Exception as e:
            logging.error(str(e))
        return revisions

    def get_key(self, key):
        return self.r.get(key)

    def get_key_map(self, key):
        return eval(self.r.get(key))

    def set_key(self, key, value):
        try:
            return self.r.set(key, value)
        except:
            return False

    def delete_key(self, key):
        return self.r.delete(key)

    def add_list_item(self, key, valus):
        self.r.lpush(key, valus)

    def get_list(self, key):
        self.r.getrange(key, 0, self.r.llen(key))

    def get_r(self):
        return self.r


if __name__ == '__main__':
    print(Redis().get_key(""))
