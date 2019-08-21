# -*- coding: UTF-8 -*-
import configparser
import logging.config
import os

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_apscheduler import APScheduler
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from com.common.getPath import Path
from com.common.model import User, Service, api_manager, test_case, task_schedul, test_report
from com.route.admin import MyView
from com.route.apis import apis
from com.route.view import view
from com.service.timeTask import TaskOperate

app = Flask(__name__)


class Main():
    def __init__(self):
        self.app = app
        self.globalspath = Path().get_current_path()
        self.app.config['SECRET_KEY'] = '123456'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.globalspath + '/static/sqlite.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
        self.app.config['SCHEDULER_API_ENABLED'] = True

        logging.config.fileConfig(self.globalspath + '/config/logger.conf')
        conf = configparser.ConfigParser()
        conf.read(self.globalspath + '/config/config.ini', encoding='utf-8')

        # 注册admin管理模块
        self.db = SQLAlchemy(self.app)
        self.bootstrap = Bootstrap(self.app)
        self.admin = Admin(self.app, name='YPSH', template_mode='bootstrap3')

        # 注册定时任务
        self.scheduler = APScheduler()
        self.scheduler.init_app(self.app)
        self.scheduler.start()

    def get_app(self):
        return self.app

    def get_crt(self):
        return os.path.join(self.globalspath, 'static/crt/server.crt')

    def get_key(self):
        return os.path.join(self.globalspath, 'static/crt/server.key')

    def add_jobs(self):
        TaskOperate().add_jobs()

    def add_admin_view(self):
        print(self.globalspath)
        self.admin.add_view(FileAdmin(self.globalspath, '', name='后台文件管理'))
        self.admin.add_view(MyView(name='返回主页', endpoint=''))
        self.admin.add_view(ModelView(User, self.db.session))
        self.admin.add_view(ModelView(Service, self.db.session))
        self.admin.add_view(ModelView(api_manager, self.db.session))
        self.admin.add_view(ModelView(test_case, self.db.session))
        self.admin.add_view(ModelView(test_report, self.db.session))
        self.admin.add_view(ModelView(task_schedul, self.db.session))

    def add_views_path(self):
        self.app.register_blueprint(view, url_prefix='/')

    def add_apis_path(self):
        self.app.register_blueprint(apis, url_prefix='/apis')


main = Main()
mapp = main.get_app()
main.add_apis_path()
main.add_views_path()
main.add_admin_view()

if __name__ == '__main__':
    # app.run(debug=False, host='0.0.0.0', threaded=True, ssl_context=(main.get_crt(), main.get_key()))
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)
    # app.run()
