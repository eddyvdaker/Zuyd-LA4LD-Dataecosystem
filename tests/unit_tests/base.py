# -*- coding: utf-8 -*-
"""
    tests.unit_tests.base
    ~~~~~~~~~~~~~~~~~~~~~

    The basic functionality for running functional tests
"""

from unittest import TestCase

import app
from config import Config


class TestConfig(Config):
    pass


class UnitTest(TestCase):
    """Base TestCase object used for unit tests."""

    def setUp(self):
        self.app = app.app

    def tearDown(self):
        pass
