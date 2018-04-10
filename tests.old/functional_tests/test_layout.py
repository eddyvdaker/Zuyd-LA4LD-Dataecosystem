# -*- coding: utf-8 -*-
"""
    tests.functional_tests.test_layout
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Functional tests for layout and pages.
"""

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest, TEST_USERNAME, TEST_PASSWORD


class LayoutTest(FunctionalTest):

    def login(self, username=TEST_USERNAME, password=TEST_PASSWORD):
        # Uses sees that it is the login page
        text = self.waitFor(lambda: self.browser.find_element_by_tag_name(
            'h1')).text
        self.assertIn('Sign In', text)

        # User types username into login field
        username_box = self.browser.find_element_by_id('username')
        username_box.send_keys(username)

        # Uses types password into login field and submits
        password_box = self.browser.find_element_by_id('password')
        password_box.send_keys(password)
        password_box.send_keys(Keys.ENTER)

    def test_home_page(self):
        # User goes to home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # User sees a page
        text = self.browser.find_element_by_tag_name('div').text
        self.assertIn('LA4LD', text)

        # User notices he/she has been redirected to the login page
        text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Sign In', text)

    def test_login_page_correct(self):
        # User goes to login page
        self.browser.get(self.live_server_url + '/login')
        self.browser.set_window_size(1024, 768)

        # User sees login page and enters details
        self.login(username='ed', password='cat')

        text = self.waitFor(lambda: self.browser.find_element_by_id(
            'welcome-text')).text
        self.assertIn('Hello', text)

    def test_login_page_invalid_user_and_pass(self):
        # User goes to login page
        self.browser.get(self.live_server_url + '/login')
        self.browser.set_window_size(1024, 768)

        # User uses wrong username AND password
        self.login(username='abc', password='abc')
        warning = self.waitFor(lambda: self.browser.find_element_by_id(
            'messages')).text
        self.assertIn('Invalid username or password', warning)

    def test_login_page_invalid_user(self):
        # User goes to login page
        self.browser.get(self.live_server_url + '/login')
        self.browser.set_window_size(1024, 768)

        # User types wrong username but correct password
        self.login(username='abc', password='cat')
        warning = self.waitFor(lambda: self.browser.find_element_by_id(
            'messages')).text
        self.assertIn('Invalid username or password', warning)

    def test_login_page_invalid_password(self):
        # User goes to login page
        self.browser.get(self.live_server_url + '/login')
        self.browser.set_window_size(1024, 768)

        # User types correct username but wrong password
        self.login(username='ed', password='abc')
        warning = self.waitFor(lambda: self.browser.find_element_by_id(
            'messages')).text
        self.assertIn('Invalid username or password', warning)

    def test_own_profile_page(self):
        self.browser.get(self.live_server_url + '/user/ed')
        self.browser.set_window_size(1024, 768)

        self.login(username='ed', password='cat')
        text = self.waitFor(lambda: self.browser.find_element_by_id(
            'profile-header')).text
        self.assertIn('Profile Page', text)

        data = self.waitFor(lambda: self.browser.find_element_by_id(
            'user-data')).text
        self.assertIn('abc', data)

    def test_other_profile_page(self):
        self.browser.get(self.live_server_url + '/user/ed')
        self.browser.set_window_size(1024, 768)

        self.login(username='test', password='dog')
        text = self.waitFor(lambda: self.browser.find_element_by_id(
            'profile-header')).text
        self.assertIn('Profile Page', text)

        data = self.waitFor(lambda: self.browser.find_element_by_id(
            'user-data')).text
        self.assertNotIn('abc', data)
