from unittest import TestCase, main

import app as flask_app
from app import db
from app.models import User, Role
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_METHODS = []


class UnitTest(TestCase):

    def setUp(self):
        app = flask_app.create_app(TestConfig)
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        # self.app_test_client = self.app.test_client()
        with self.app_context:
            db.create_all()

        # Create test roles
        roles = ['admin', 'student', 'teacher']
        for role in roles:
            r = Role(role=role)
            db.session.add(r)
        db.session.commit()

        # Create test users
        for i, role in enumerate(roles):
            u = User(username=f'usr{i}', email=f'usr{i}@la4ld-test.com')
            db.session.add(u)
            db.session.commit()

            u.set_password('cat')
            r = Role.query.filter_by(role=role).first()
            u.role_id = r.id
            db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == '__main__':
    main(verbosity=2)

