# -*- coding: UTF-8 -*-
import logging
import os
import time
from datetime import datetime

from com.common.model import files_manager, db


class FilesManager:

    def get_all(self):
        return files_manager.query.all()

    def get_all_by_filepath(self, file_path):
        return files_manager.query.filter_by(file_path=file_path)

    def get_file_name(self, id):
        result = files_manager.query.filter_by(id=id).first()
        return result.file_name

    def get_file_path(self, id):
        result = files_manager.query.filter_by(id=id).first()
        return result.file_path

    def get_list(self, file_path):
        data = []
        try:
            result = self.get_all_by_filepath(file_path)
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
                                 item.file_path,
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
                                  file_path=data['file_path'],
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
                        service.remark = data[8]
                    db.session.flush()
            db.session.commit()
            db.session.close()
            return {"message": True}

        except Exception as e:
            db.session.close()
            return {"message": str(e)}

    def get_report(self, file_path):
        data = []
        try:
            dirs = os.listdir(file_path)
            for dir in dirs:
                create_time = os.path.getctime(os.path.join(file_path, dir))
                timeStruct = time.localtime(create_time)
                create_time = time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)
                size = os.path.getsize(os.path.join(file_path, dir))
                report=os.path.join(file_path,dir,'result/index.html')
                log=os.path.join(file_path,dir,'jmeter.log')
                data.append([dir, create_time, report,log])
            return data
        except Exception as e:
            logging.error(str(e))
            return data
