# -*- coding: utf-8 -*-
"""
    tests.unit.base
    ~~~~~~~~~~~~~~~

    Base functionality for running unit tests
"""
from unittest import TestCase, main

from app import create_app, db
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UnitTest(TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == '__main__':
    main(verbosity=2)
