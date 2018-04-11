# -*- coding: utf-8 -*-
"""
    tests.unit.test_models
    ~~~~~~~~~~~~~~~~~~~~~~

    Unit tests for the SQLAlchemy models
"""
from sqlalchemy.exc import IntegrityError

from tests.unit.base import UnitTest

from app import db
from app.models import User, Role


class UserModelTest(UnitTest):

    def create_test_user(self):
        user = User(username='abc', email='abc@abc.com')
        db.session.add(user)
        db.session.commit()
        return user

    def create_test_role(self):
        role = Role(role='test_role')
        db.session.add(role)
        db.session.commit()

    def test_create_user(self):
        """Tests the creation of a new user"""
        self.create_test_user()

    def test_try_to_add_duplicate_user(self):
        """Tests if adding a duplicate user raises an error"""
        self.create_test_user()
        with self.assertRaises(IntegrityError):
            user = self.create_test_user()
            db.session.add(user)
            db.session.commit()

    def test_add_role_to_user(self):
        """Tests if a role can be assigned to a user"""
        user = self.create_test_user()
        self.create_test_role()
        user.role_id = 1
        db.session.commit()

    def test_password(self):
        """Tests the setting and retrieving of passwords"""
        user = self.create_test_user()
        user.set_password('cat')
        db.session.commit()
        self.assertFalse(user.check_password('dog'))
        self.assertTrue(user.check_password('cat'))

    def test_reset_token(self):
        """Tests the generation and validation of reset tokens"""
        user = self.create_test_user()
        token = user.get_reset_password_token()
        wrong_token = user.verify_reset_password_token('abc')
        if wrong_token:
            raise Exception('wrong token still verified')
        right_token = user.verify_reset_password_token(token)
        if not right_token:
            raise Exception('right token not verified')


class RoleModelTest(UnitTest):

    def test_create_role(self):
        """Tests the creation of new roles"""
        role = Role(role='test_role')
        db.session.add(role)
        db.session.commit()

    def test_try_to_add_duplicate_role(self):
        """Tests if a duplicate role raises an error"""
        role = Role(role='test_role')
        db.session.add(role)
        db.session.commit()
        with self.assertRaises(IntegrityError):
            role = Role(role='test_role')
            db.session.add(role)
            db.session.commit()
