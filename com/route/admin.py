# -*- coding: UTF-8 -*-
import os.path as op

from flask import Flask, render_template
from flask_admin import Admin, BaseView, expose

app = Flask(__name__)
admin = Admin(app)


class MyView(BaseView):
    @expose('/')
    def index(self):
        return render_template('index.html')


path = op.join(op.dirname(__file__), 'static')

if __name__ == '__main__':
    app.run()
