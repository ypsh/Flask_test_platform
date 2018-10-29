# -*- coding: UTF-8 -*-
import logging
from datetime import datetime

from com.common.model import files_manager, db


class FilesManager:

    def get_all(self):
        return files_manager.query.all()

    def get_file_name(self, id):
        result = files_manager.query.filter_by(id=id).first()
        return result.file_name

    def get_list(self):
        data = []
        try:
            result = self.get_all()
            if result:
                for item in result:
                    size = str(item.file_size / 1024).split('.')
                    if size.__len__() == 2:
                        size = size[0] + size[1][0:1]
                    else:
                        size = size[0]
                    data.append([item.id,
                                 item.file_name,
                                 item.file_type,
                                 size + ' kb',
                                 item.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                                 item.creater,
                                 item.remark])
                return data
        except Exception as e:
            logging.error(str(e))
            return None

    def add_file(self, *args):
        try:
            for data in args:
                db.session.add(
                    files_manager(file_name=data['file_name'],
                                  file_type=data['file_type'],
                                  file_size=data['file_size'],
                                  creater=data['user'],
                                  remark=data['remark'],
                                  create_time=datetime.now()
                                  )
                )
            db.session.commit()
            db.session.close()
            return True

        except Exception as e:
            logging.error(str(e))
            return False

    def del_items(self, *args):
        try:
            for item in args:
                for data in item:
                    service = files_manager.query.filter_by(id=data[0]).first()
                    db.session.delete(service)
            db.session.commit()
            db.session.close()
            return True
        except Exception as e:
            db.session.close()
            logging.error(str(e))
            return False

    def batch_update(self, *args):
        try:
            for item in args:
                for data in item:
                    service = files_manager.query.filter_by(id=data[0]).first()
                    if service:
                        service.remark = data[7]
                    db.session.flush()
            db.session.commit()
            db.session.close()
            return {"message": True}

        except Exception as e:
            db.session.close()
            return {"message": str(e)}
