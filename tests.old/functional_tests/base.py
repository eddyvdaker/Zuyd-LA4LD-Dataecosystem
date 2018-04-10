# -*- coding: utf-8 -*-
"""
    tests.functional_tests.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The basic functionality for running functional tests
"""

import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from unittest import TestCase
from time import sleep, time

MAX_WAIT = 5
TEST_USERNAME = 'test'
TEST_PASSWORD = 'test_password'
TEST_EMAIL = 'test@test.com'


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

    def assertInList(self, element, list_to_check):
        """
        Version of assertIn that iterates over a list and checks if it
        contains a certain element

        :param element: <str> Element that needs to be checked for
        :param list_to_check: <list> List of elements
        """
        result = False
        for item in list_to_check:
            if element in item:
                result = True
        if not result:
            raise AssertionError(f'\'{element}\' not found in list '
                                 f'{list_to_check}')

    def waitFor(self, fn):
        """
        Keeps checking for element to catch situations where the test runs
        faster than the page loading.

        :param fn: element to search for
        :return: element that is being searched for, or raises an assertion
        error if the element is not found.
        """
        start_time = time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time() - start_time > MAX_WAIT:
                    raise e
                sleep(0.5)
