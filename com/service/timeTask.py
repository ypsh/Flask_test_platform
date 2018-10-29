# -*- coding: UTF-8 -*-
import logging

from flask import current_app

from com.common.getPath import Path
from com.common.mailUtil import SentMail
from com.common.model import task_schedul
from com.service.executeCase import ExecuteCase


class TaskOperate:
    def __init__(self):
        self.tasks = self.get_alltask()
        global_path = Path().get_current_path()
        self.url = 'sqlite:///' + global_path + '/static/sqlite.db'

    def get_alltask(self):
        result = task_schedul().query.all()
        task = []
        if result:
            for item in result:
                task.append({'id': str(item.id) + item.schedul_name, 'model': item.model, 'frequency': item.frequency,
                             'trigger': item.trigger, 'until': item.until, 'start_time': item.start_time})
        return task

    def run_all(self):
        logging.info('开始执行所有用例')
        data = {'type': 'all', 'user': 'System', 'environment': '测试环境'}
        result = ExecuteCase().execute_cases(data)
        logging.info('执行完成')
        SentMail().snd_report(result)

    def run_model(self, model):
        logging.info('开始执行所有用例')
        data = {'type': 'model', 'user': 'Admin', 'environment': '测试环境', 'data': model}
        result = ExecuteCase().execute_cases(data)
        logging.info('执行完成')
        SentMail().snd_report(result)

    def remove_job(self, job_id):
        try:
            current_app.apscheduler.remove_job(job_id)
            return True
        except Exception as e:
            logging.error(str(e))
            return None

    def add_jobs(self):
        try:
            tasks = self.get_jobs()
            if tasks is not None:
                for item in tasks:
                    self.remove_job(item[0])
            for item in self.tasks:
                if item['model'] == 'all' and item['trigger'] == 'interval':
                    if item['until'] == 'seconds':
                        current_app.apscheduler.add_job(func=self.run_all, id=item['id'], trigger='interval',
                                                        seconds=item['frequency'])
                    elif item['until'] == 'minutes':
                        current_app.apscheduler.add_job(func=self.run_all, id=item['id'], trigger='interval',
                                                        minutes=item['frequency'])
                    elif item['until'] == 'hours':
                        current_app.apscheduler.add_job(func=self.run_all, id=item['id'], trigger='interval',
                                                        hours=item['frequency'])
                    elif item['until'] == 'days':
                        current_app.apscheduler.add_job(func=self.run_all, id=item['id'], trigger='interval',
                                                        days=item['frequency'])
                elif item['model'] == 'all' and item['trigger'] == 'date':
                    current_app.apscheduler.add_job(func=self.run_all, id=item['id'], trigger='date',
                                                    run_date=item['start_time'])
                elif item['model'] != 'all' and item['trigger'] == 'interval':
                    if item['until'] == 'seconds':
                        current_app.apscheduler.add_job(func=self.run_model, id=item['id'], trigger='interval',
                                                        seconds=item['frequency'], args=[item['model']])
                    elif item['until'] == 'minutes':
                        current_app.apscheduler.add_job(func=self.run_model, id=item['id'], trigger='interval',
                                                        minutes=item['frequency'], args=[item['model']])
                    elif item['until'] == 'hours':
                        current_app.apscheduler.add_job(func=self.run_model, id=item['id'], trigger='interval',
                                                        hours=item['frequency'], args=[item['model']])
                    elif item['until'] == 'days':
                        current_app.apscheduler.add_job(func=self.run_model, id=item['id'], trigger='interval',
                                                        days=item['frequency'], args=[item['model']])
                elif item['model'] != 'all' and item['trigger'] == 'date':
                    current_app.apscheduler.add_job(func=self.run_model, id=item['id'], trigger='date',
                                                    run_date=item['start_time'], args=[item['model']])
                elif item['model'] == 'all' and item['trigger'] == 'cron':
                    current_app.apscheduler.add_job(func=self.run_all, id=item['id'], trigger='cron',
                                                    hour=item['frequency'])
                elif item['model'] != 'all' and item['trigger'] == 'cron':
                    current_app.apscheduler.add_job(func=self.run_model, id=item['id'], trigger='cron',
                                                    hour=item['frequency'], args=[item['model']])
            return True
        except Exception as e:
            logging.error(str(e))
            return False

    def get_jobs(self):
        try:
            jobs = []
            result = current_app.apscheduler.get_jobs()
            if result:
                for item in result:
                    if str(item.trigger).find('date') != 0:
                        if item.trigger.start_date is not None:
                            start_time = item.trigger.start_date.strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            start_time = ''
                    else:
                        start_time = ''
                    jobs.append([item.id, item.name, str(item.args), item.func_ref,
                                 start_time, item.next_run_time.strftime('%Y-%m-%d %H:%M:%S'),
                                 str(item.trigger)])
                return jobs
        except Exception as e:
            logging.error(str(e))
            return None

    if __name__ == '__main__':
        pass
