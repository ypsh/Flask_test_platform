# -*- coding: UTF-8 -*-
import datetime
import logging

from com.common.model import db
from com.common.model import task_schedul
from com.common.model import test_case


class TaskSchedul:
    def get_all(self):
        return task_schedul.query.all()

    def get_one(self, api_name):
        result = task_schedul.query.filter_by(api_name=api_name).first()
        if result is not None:
            return {'api_name': result.api_name, 'model': result.model, 'type': result.type,
                    'path': result.path, 'headers': result.headers, 'status': result.status, 'maker': result.mark}
        else:
            return None

    def get_list(self):
        data = []
        try:
            result = self.get_all()
            if result:
                for item in result:
                    if item.start_time is not None:
                        start_time = item.start_time.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        start_time = ''
                    data.append([
                        item.id,
                        item.schedul_name,
                        item.model,
                        item.trigger,
                        start_time,
                        item.frequency,
                        item.until,
                        item.creater,
                        item.create_time.strftime("%Y-%m-%d %H:%M:%S")
                    ])
            return data
        except Exception as e:
            logging.error(str(e))
            return data

    def del_item(self, task_id):
        try:
            service = task_schedul.query.filter_by(id=task_id).first()
            if service:
                db.session.delete(service)
                db.session.commit()
                db.session.close()
                return {"message": True}
            else:
                return {"message": False}
        except Exception as e:
            db.session.close()
            return {"message": str(e)}

    def add_task(self, *args):
        create_time = datetime.datetime.now()
        try:
            for item in args:
                if item['start_time'] != '':
                    start_time = datetime.datetime.strptime(item['start_time'], "%Y-%m-%d %H:%M:%S")
                else:
                    start_time = None
                admin = task_schedul(
                    schedul_name=item['task_name'],
                    model=item['model'],
                    trigger=item['trigger'],
                    start_time=start_time,
                    frequency=item['frequency'],
                    until=item['until'],
                    creater=item['user'],
                    create_time=create_time
                )
                db.session.add(admin)
            db.session.commit()
            db.session.close()
            return {"message": True}

        except Exception as e:
            db.session.close()
            return {"message": str(e)}

    def update_task(self, *args):
        try:
            for item in args:
                result = task_schedul.query.filter_by(id=item['task_id']).first()
                if item['trigger'] == 'date':
                    start_time = datetime.datetime.strptime(item['start_time'], "%Y-%m-%d %H:%M:%S")
                    frequency = ''
                    until = ''
                else:
                    start_time = None
                    frequency = item['frequency']
                    until = item['until']
                if result:
                    result.schedul_name = item['task_name']
                    result.model = item['model']
                    result.trigger = item['trigger']
                    result.start_time = start_time
                    result.frequency = frequency
                    result.until = until
                    db.session.flush()
            db.session.commit()
            db.session.close()
            return {"message": True}

        except Exception as e:
            db.session.close()
            return {"message": str(e)}


if __name__ == '__main__':
    test_case().get_all()
