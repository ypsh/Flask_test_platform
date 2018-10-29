# -*- coding: UTF-8 -*-
import datetime
import logging

from com.common.model import db
from com.common.model import test_case
from com.common.model import test_report


class TestReportOperate:
    def get_all(self):
        return test_report.query.all()

    def get_one(self, api_name):
        result = test_report.query.filter_by(api_name=api_name).first()
        if result is not None:
            return {'api_name': result.api_name, 'model': result.model, 'type': result.type,
                    'path': result.path, 'headers': result.headers, 'status': result.status, 'maker': result.mark}
        else:
            return None

    def add_report(self, *args):
        create_time = datetime.datetime.now()
        try:
            for item in args:
                for report in item:
                    admin = test_report(
                        case_id=report['case_id'],
                        start_time=report['start_time'],
                        end_time=report['end_time'],
                        input=report['input'],
                        response_result=report['response_result'],
                        expect_result=report['expect_result'],
                        response_status=report['response_status'],
                        request_type=report['request_type'],
                        response_headers=report['response_headers'],
                        response_path=report['response_path'],
                        creater=report['creater'],
                        validation_type=report['validation_type'],
                        validation_result=report['validation_result'],
                        api_name=report['api_name'],
                        model=report['model'],
                        case_name=report['case_name'],
                        use_time=report['use_time'],
                        batch_number=report['batch_number'],
                        execute_type=report['execute_type'],
                        create_time=create_time
                    )
                    db.session.add(admin)
            db.session.commit()
            db.session.close()
            return {"message": True}

        except Exception as e:
            db.session.close()
            return {"message": str(e)}

    def get_report_data(self, *args):
        try:
            data = {}
            filters = []
            performance = []
            casename = []
            table = []
            details = []
            if args[0].source == '' or args[0].source == 'last':
                batch_number = test_report.query.order_by((test_report.batch_number.desc())).first().batch_number
                filters.append(test_report.batch_number == batch_number)
            elif args[0].source == 'all':
                if args[0].creater != '':
                    filters.append(test_report.creater == args[0].creater)
                if args[0].batchnumber != '':
                    filters.append(test_report.batch_number.like('%' + args[0].batchnumber + '%'))
                if args[0].executetype != '':
                    filters.append(test_report.execute_type == args[0].executetype)
                if args[0].daterange != '':
                    time = args[0].daterange.split('-')
                    starttime = datetime.datetime.strptime(time[0][0:-1], "%Y/%m/%d %H:%M")
                    endtime = datetime.datetime.strptime(time[1][1:], "%Y/%m/%d %H:%M")
                    filters.append(test_report.create_time < endtime)
                    filters.append(test_report.create_time > starttime)
            elif args[0].source == 'lastmodel':
                batch_number = test_report.query.order_by((test_report.batch_number.desc())).filter_by(
                    execute_type='model').first().batch_number
                filters.append(test_report.batch_number == batch_number)
            elif args[0].source == 'lastselect':
                batch_number = test_report.query.order_by((test_report.batch_number.desc())).filter_by(
                    execute_type='select').first().batch_number
                filters.append(test_report.batch_number == batch_number)
            elif args[0].source == 'lastall':
                batch_number = test_report.query.order_by((test_report.batch_number.desc())).filter_by(
                    execute_type='all').first().batch_number
                filters.append(test_report.batch_number == batch_number)

            query = test_report.query.filter(*filters).order_by(test_report.start_time.desc())
            result = query.all()
            if result:
                data['user'] = result[0].creater
                data['create_time'] = result[0].create_time.strftime('%Y-%m-%d %H:%M:%S')
                data['pass'] = query.filter(test_report.validation_result == 'PASS').all().__len__()
                data['fail'] = query.filter(test_report.validation_result == 'FAIL').all().__len__()
                total = result.__len__()
                data['total'] = total
                for i in range(0, total):
                    casename.append(result[i].case_name)
                    performance.append(result[i].use_time / 1000)
                    tableline = [
                        i + 1,
                        result[i].id,
                        result[i].batch_number,
                        result[i].case_name,
                        result[i].model,
                        result[i].api_name,
                        result[i].response_status,
                        result[i].validation_result,
                        (result[i].use_time / 1000),
                        result[i].create_time.strftime('%Y-%m-%d %H:%M:%S'),
                        result[i].creater
                    ]
                    detail = [
                        result[i].id,
                        result[i].batch_number,
                        result[i].case_name,
                        result[i].api_name,
                        result[i].model,
                        result[i].response_path,
                        result[i].response_status,
                        (result[i].use_time / 1000),
                        result[i].creater,
                        result[i].validation_type,
                        result[i].validation_result,
                        result[i].input,
                        result[i].response_headers,
                        result[i].expect_result,
                        result[i].response_result,
                        result[i].request_type
                    ]
                    table.append(tableline)
                    details.append(detail)
                data['table'] = table
                data['performance'] = performance
                data['casenames'] = casename
                data['usetime'] = (result[0].end_time - result[total - 1].start_time).seconds
                data['details'] = details

            return data
        except Exception as e:
            logging.error(str(e))
            return None

    def get_createrlist(self):
        result = test_report.query.with_entities(test_report.creater).distinct().all()
        cteaters = []
        if result:
            for item in result:
                cteaters.append(item[0])
        return cteaters


if __name__ == '__main__':
    test_case().get_all()
