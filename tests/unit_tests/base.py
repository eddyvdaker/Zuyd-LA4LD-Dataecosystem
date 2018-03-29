# -*- coding: utf-8 -*-
"""
    tests.unit_tests.base
    ~~~~~~~~~~~~~~~~~~~~~

    The basic functionality for running functional tests
"""

import os
from flask_testing import TestCase as TestCase
from flask_login import login_user, logout_user

from app import app, db
from app.models import User
from config import Config

BASE_DIR = basedir = os.path.abspath(os.path.dirname(__file__))
BASE_URL = 'http://127.0.0.1:5000'
TEST_USERNAME = 'test'
TEST_PASSWORD = 'test_password'
TEST_EMAIL = 'test@test.com'


class TestConfig(Config):
    pass


class UnitTest(TestCase):
    """TestCase object used for view and controller tests"""

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
        u = User(username=TEST_USERNAME, email=TEST_EMAIL)
        u.set_password(TEST_PASSWORD)
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username=TEST_USERNAME):
        user = User.query.filter_by(username=username).first()
        if user:
            login_user(user)

    def logout(self):
        logout_user()
