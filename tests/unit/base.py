# -*- coding: utf-8 -*-
"""
    tests.unit.base
    ~~~~~~~~~~~~~~~

    Base functionality for running unit tests
"""
from flask_login import login_user, logout_user
from flask_testing import TestCase as FlaskTestCase
from unittest import TestCase, main

import app as flask_app
from app import db
from app.models import User, Role
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UnitTest(TestCase):

    def setUp(self):
        self.app = flask_app.create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class ViewUnitTest(FlaskTestCase):

    def create_app(self):
        app = flask_app.create_app(TestConfig)
        return app

    def setUp(self):
        self.app = self.create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_roles(self):
        r1 = Role(role='admin')
        r2 = Role(role='student')
        r3 = Role(role='teacher')
        db.session.add_all([r1, r2, r3])
        db.session.commit()

    def create_user(self, role):
        nr_users = len(User.query.all())
        user = User(username=f'usr{nr_users + 1}',
                    email=f'usr{nr_users}@la4ld-test.com')
        db.session.add(user)
        db.session.commit()

        user.set_password('cat')
        user.role_id = Role.query.filter_by(role=role).first()
        db.session.commit()
        return user

    def login_user(self, role='admin'):
        if len(Role.query.all()) == 0:
            self.create_roles()
        user = self.create_user(role)
        login_user(user)

    def logout_user(self):
        logout_user()


if __name__ == '__main__':
    main(verbosity=2)

