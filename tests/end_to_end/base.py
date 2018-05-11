# -*- coding: utf-8 -*-
"""
    tests.end-to-end.base
    ~~~~~~~~~~~~~~~~~~~~~

    Basic functionality for running end-to-end tests
"""

import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from unittest import TestCase
from time import sleep, time


MAX_WAIT = 5


class EndToEndTest(TestCase):

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

        :param element: Element to check for
        :param list_to_check: List of elements
        """
        result = False
        for item in list_to_check:
            if element in item:
                result = True
        if not result:
            raise AssertionError(
                f'\'{element}\' not found in list ' f'{list_to_check}'
            )

    def waitFor(self, fn):
        """
        Keeps checking for element to catch situations where the test runs
        faster than the page loading

        :param fn: element to search for
        """
        start_time = time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time() - start_time > MAX_WAIT:
                    raise e
                sleep(0.5)

    def loginUser(self, username, password):
        """
        Logs in a user

        :param username: users username
        :param password: users password
        """
        self.browser.get(self.live_server_url + '/login')
        username_input = self.browser.find_element_by_id('username')
        password_input = self.browser.find_element_by_id('password')
        submit_input = self.browser.find_element_by_id('submit')

        username_input.send_keys(username)
        password_input.send_keys(password)
        submit_input.send_keys(Keys.ENTER)
        sleep(0.5)
