# -*- coding: utf-8 -*-
"""
    tests.unit_tests.test_models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Unit tests for the models
"""

from .base import BASE_URL, UnitTest

from app.models import User


class UserModelTest(UnitTest):

    def test_create_user(self):
        """Tests the creation of a new user."""
        user = User(username='abc', email='abc@abc.com')

    def test_password(self):
        """Test setting password for new user"""
        user = User(username='abc2', email='abc2@abc.com')
        user.set_password('xyz')
        self.assertTrue(user.check_password('xyz'))
