# -*- coding: UTF-8 -*-
from com.common.model import Service
from com.common.model import db


class ServiceOperate:
    def get_all(self, page, limit):
        return Service.query.paginate(page, per_page=limit)

    def get_service(self, service_name):
        service = Service.query.filter_by(service_name=service_name).first()
        if service is not None:
            return {'service_name': service.service_name, 'type': service.type,
                    'data': service.data, 'path': service.path, 'status': service.status, 'creater': service.creater}
        else:
            return None

    def add_service(self, *args):
        try:
            admin = Service(
                service_name=args[0]['service_name'],
                type=args[0]['type'],
                data=args[0]['data'],
                path=args[0]['path'],
                status=args[0]['status'],
                creater=args[0]['user']
            )
            db.session.add(admin)
            db.session.commit()
            return True
        except Exception as e:
            db.session.close()
            return False

    def update_service(self, *args):
        try:
            service = Service.query.filter_by(id=args[0]['id']).first()
            if service:
                service.service_name = args[0]['service_name']
                service.type = args[0]['type']
                service.data = args[0]['data']
                service.path = args[0]['path']
                service.status = args[0]['status']
                service.updater = args[0]['user']
                db.session.flush()
                db.session.commit()
                db.session.close()
            return True
        except Exception as e:
            return False

    def del_item(self, id):
        try:
            service = Service.query.filter_by(id=id).first()
            db.session.delete(service)
            db.session.commit()
            db.session.close()
            return {"message": True}
        except Exception as e:
            return {"message": str(e)}

    def get_mock_list(self, page, limit):
        result = []
        data = self.get_all(page, limit)
        if data is not None:
            for item in data.items:
                line = {'id': item.id, 'serviceName': str(item.service_name), 'requestType': item.type,
                        'servicePath': item.path, 'response': item.data, 'status': item.status, 'creator': item.creater}
                result.append(line)
        return {'data': result, 'total': data.total}


if __name__ == '__main__':
    ServiceOperate().get_all()
