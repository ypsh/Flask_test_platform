# -*-coding:utf-8-*-
import configparser
import logging
import logging.config

from rediscluster import StrictRedisCluster

from com.common.getPath import Path

'''
redis 配置
'''


class Redis:
    global_path = Path().get_current_path()
    logging.config.fileConfig(global_path + '/config/logger.conf')
    password = ''

    def get_nodes(self):
        nodes = []
        try:
            conf = configparser.ConfigParser()
            conf.read(self.global_path + '/config/config.ini',encoding='utf-8')
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
            revisions = StrictRedisCluster(startup_nodes=redis_nodes, password=self.password)
        except Exception as e:
            logging.error(str(e))
        return revisions

    def get_key(self, key):
        return self.config_redis().get(key)


if __name__ == '__main__':
    print(Redis().get_key(""))
