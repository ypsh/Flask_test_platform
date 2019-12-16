# -*- coding: UTF-8 -*-
from com.common.model import User
from com.common.model import db


class UserOperate():
    def get_alluser(self):
        return User.query.all()

    def get_user(self, user):
        user = User.query.filter_by(user=user).first()
        if user is not None:
            return {'id': user.id, 'user': user.user, 'password': user.password, 'avatar': user.image,'roles':['admin'],'introduction':'固定管理员权限'}
        else:
            return None

    def add_user(self, user):
        admin = User(user)
        db.session.add(admin)
        db.session.commit()

    def del_user(self, user):
        admin = self.get_user(user)
        db.session.delete(admin)
        db.session.commit()


if __name__ == '__main__':
    UserOperate().get_alluser()
