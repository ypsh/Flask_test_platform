import configparser
import logging

from com.common.getPath import Path


class Set_url:
    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.globalpath = Path().get_current_path()
        self.conf.read(self.globalpath + '/config/config.ini', encoding='utf-8')

    def get_url(self, project):
        try:
            url = self.conf.get('project_env', project)
            return url
        except Exception as e:
            return None

    def add_url(self,project,url):
        try:
            if project!='':
                self.conf.set('project_env', project, url)
                self.conf.write(open(self.globalpath + '/config/config.ini', 'w', encoding='utf-8'))
                return True
            else:
                return False
        except Exception as e:
            logging.error(str(e))
            return False


if __name__ == '__main__':
    Set_url().get_url('网名')
    Set_url().add_url('网名','http:test')
