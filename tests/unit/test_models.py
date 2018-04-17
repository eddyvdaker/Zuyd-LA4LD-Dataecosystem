# -*- coding: utf-8 -*-
"""
    tests.unit.test_models
    ~~~~~~~~~~~~~~~~~~~~~~

    Unit tests for the SQLAlchemy models
"""
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from tests.unit.base import UnitTest

from app import db
from app.models import User, Role, Module


class UserModelTest(UnitTest):

    def create_test_user(self):
        user = User(username='abc', email='abc@abc.com', card_number="123")
        db.session.add(user)
        db.session.commit()
        return user

    def create_test_role(self):
        role = Role(role='test_role')
        db.session.add(role)
        db.session.commit()

    def create_test_module(self):
        module = Module(code='tm01')
        db.session.add(module)
        db.session.commit()
        return module

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

    def test_add_to_module_as_student(self):
        """Tests if students can be added to modules"""
        user = self.create_test_user()
        module = self.create_test_module()
        user.add_to_module(module)
        assert user.student_of_module(module)
        assert module in user.get_modules_of_student()

    def test_add_to_module_as_teacher(self):
        """Tests if teachers can be added to modules"""
        user = self.create_test_user()
        module = self.create_test_module()
        user.add_to_module(module, module_role='teacher')
        assert user.teacher_of_module(module)
        assert module in user.get_modules_of_teacher()

    def test_add_to_module_as_examiner(self):
        """Tests if examiners can be added to modules"""
        user = self.create_test_user()
        module = self.create_test_module()
        user.add_to_module(module, module_role='examiner')
        assert user.examiner_of_module(module)
        assert module in user.get_modules_of_examiner()


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


class ModuleModelTest(UnitTest):

    def test_create_module(self):
        """Test if new modules can be created"""
        module = Module(
            code='tm01',
            name='testmodule01',
            description='This is a test module',
            start=datetime(2009, 10, 1),
            end=datetime(2010, 10, 1),
            faculty='Faculteit ICT',
        )
        db.session.add(module)
        db.session.commit()
