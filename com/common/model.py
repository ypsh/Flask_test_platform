# -*- coding: UTF-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from com.common.getPath import Path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + Path().get_current_path() + '/static/sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    image = db.Column(db.String)
    role = db.Column(db.String)
    email = db.Column(db.String)
    mobile = db.Column(db.String)
    is_active = db.Column(db.String)

    # create_time = db.Column(db.String)

    def __init__(self, *args):
        self.user = args

    def __repr__(self):
        return '<User %r>' % self.user

    def verify_password(self, password):
        user = User.query.filter_by(user=self.user).first()
        if str(user.password) == password:
            return True
        return False

    def get(self, id):
        return self.id


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(80), unique=True)
    path = db.Column(db.String(240))
    type = db.Column(db.String)
    data = db.Column(db.Text)
    status = db.Column(db.String)
    creater = db.Column(db.String)
    updater = db.Column(db.String)

    def __repr__(self):
        return '<Service %r>' % self.service_name

    def get(self, id):
        return self.id


class api_manager(db.Model):
    __tablename__ = 'api_manager'

    id = db.Column(db.Integer, primary_key=True)
    api_name = db.Column(db.String, unique=True)
    model = db.Column(db.String)
    type = db.Column(db.String)
    path = db.Column(db.String)
    status = db.Column(db.String)
    headers = db.Column(db.String)
    need_token = db.Column(db.String)
    mark = db.Column(db.Text)
    cases = relationship('test_case')
    creater = db.Column(db.String)
    updater = db.Column(db.String)
    update_time = db.Column(db.TIMESTAMP)

    def __repr__(self):
        return '<api_manger %r>' % self.api_name

    def get(self, id):
        return self.id


# noinspection PyUnusedLocal
class test_case(db.Model):
    __tablename__ = 'test_case'

    id = db.Column(db.Integer, primary_key=True)
    case_name = db.Column(db.Text)
    api_id = Column(Integer, ForeignKey('api_manager.id'))
    parameter = db.Column(db.Text)
    result = db.Column(db.Text)
    validation_type = db.Column(db.String)
    mark = db.Column(db.Text)
    api = relationship('api_manager')
    creater = db.Column(db.String)
    updater = db.Column(db.String)
    update_time = db.Column(db.TIMESTAMP)
    execute_time = db.Column(db.TIMESTAMP)
    executer = db.Column(db.String)
    last_result = db.Column(db.String)

    # test_report = relationship('test_report')

    def __repr__(self):
        # return '<test_case %r>' % self.id
        return '%s(%r)' % (self.__class__.__name__, self.id)

    def get(self, id):
        return self.id


class test_report(db.Model):
    __tablename__ = 'test_report'

    id = db.Column(db.Integer, primary_key=True)
    case_id = Column(Integer)
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    input = db.Column(db.Text)
    response_result = db.Column(db.Text)
    response_status = db.Column(db.String)
    response_headers = db.Column(db.Text)
    response_path = db.Column(db.String)
    request_type = db.Column(db.String)
    creater = db.Column(db.String)
    validation_type = db.Column(db.String)
    validation_result = db.Column(db.String)
    create_time = db.Column(db.TIMESTAMP)
    api_name = db.Column(db.Text)
    model = db.Column(db.Text)
    case_name = db.Column(db.Text)
    use_time = db.Column(db.Text)
    expect_result = db.Column(db.Text)
    batch_number = db.Column(db.String)
    execute_type = db.Column(db.String)

    # cases = relationship('test_case')

    def __repr__(self):
        # return '<test_case %r>' % self.id
        return '%s(%r)' % (self.__class__.__name__, self.id)

    def get(self, id):
        return self.id


class task_schedul(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedul_name = db.Column(db.String)
    model = db.Column(db.String)
    trigger = db.Column(db.String)
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    frequency = db.Column(db.Integer)
    until = db.Column(db.String)
    creater = db.Column(db.String)
    create_time = db.Column(db.TIMESTAMP)

    def __repr__(self):
        # return '<test_case %r>' % self.id
        return '%s(%r)' % (self.__class__.__name__, self.id)

    def get(self, id):
        return self.id


class files_manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String)
    file_type = db.Column(db.String)
    file_size = db.Column(db.String)
    creater = db.Column(db.String)
    remark = db.Column(db.String)
    create_time = db.Column(db.TIMESTAMP)

    def __repr__(self):
        # return '<test_case %r>' % self.id
        return '%s(%r)' % (self.__class__.__name__, self.id)

    def get(self, id):
        return self.id


if __name__ == '__main__':
    admin = User("test", "12334")
    users = User.query.all()
    print(users)
    app.run()
