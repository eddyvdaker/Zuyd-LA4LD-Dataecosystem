# -*- coding: utf-8 -*-
"""
    tests.functional_tests.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The basic functionality for running functional tests
"""

import os
from selenium import webdriver
from unittest import TestCase


class FunctionalTest(TestCase):
    """Base TestCase object used for functional tests."""

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        else:
            self.live_server_url = 'http://127.0.0.1:5000'

    def tearDown(self):
        self.browser.quit()
